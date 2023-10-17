# coding=utf-8
# Copyright 2022 EleutherAI and the HuggingFace Inc. team. All rights reserved.
#
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" PyTorch SENTIA model."""
import math
from typing import List, Optional, Tuple, Union

import torch
import torch.nn.functional as F
import torch.utils.checkpoint
from torch import nn
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss

from transformers.activations import ACT2FN
from transformers.modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast, \
    SequenceClassifierOutputWithPast, Seq2SeqLMOutput, BaseModelOutputWithPastAndCrossAttentions
from transformers.modeling_utils import PreTrainedModel, is_torch_fx_proxy
from transformers.utils import add_start_docstrings, add_start_docstrings_to_model_forward, logging, \
    replace_return_docstrings
from .config_sentia import SENTIAConfig
import sacrebleu
import os
import warnings
from tqdm import tqdm
import wandb

# torch.set_anomaly_enabled(True)

# Most of this model is copied from transformers.models.llama.modeling_llama

logger = logging.get_logger(__name__)

_CONFIG_FOR_DOC = "SENTIAConfig"


# Copied from transformers.models.bart.modeling_bart._make_causal_mask
def _make_causal_mask(
        input_ids_shape: torch.Size, dtype: torch.dtype, device: torch.device, past_key_values_length: int = 0
):
    """
    Make causal mask used for bi-directional self-attention.
    """
    bsz, tgt_len = input_ids_shape
    mask = torch.full((tgt_len, tgt_len), torch.finfo(dtype).min, device=device)
    mask_cond = torch.arange(mask.size(-1), device=device)
    mask.masked_fill_(mask_cond < (mask_cond + 1).view(mask.size(-1), 1), 0)
    mask = mask.to(dtype)

    if past_key_values_length > 0:
        mask = torch.cat([torch.zeros(tgt_len, past_key_values_length, dtype=dtype, device=device), mask], dim=-1)
    return mask[None, None, :, :].expand(bsz, 1, tgt_len, tgt_len + past_key_values_length)


# Copied from transformers.models.bart.modeling_bart._expand_mask
def _expand_mask(mask: torch.Tensor, dtype: torch.dtype, tgt_len: Optional[int] = None):
    """
    Expands attention_mask from `[bsz, seq_len]` to `[bsz, 1, tgt_seq_len, src_seq_len]`.
    """
    bsz, src_len = mask.size()
    tgt_len = tgt_len if tgt_len is not None else src_len

    expanded_mask = mask[:, None, None, :].expand(bsz, 1, tgt_len, src_len).to(dtype)

    inverted_mask = 1.0 - expanded_mask

    return inverted_mask.masked_fill(inverted_mask.to(torch.bool), torch.finfo(dtype).min)
class SENTIASequential(nn.Sequential):
    @staticmethod
    def is_key_duplicate(dictionary, key_to_check):
            count = 0
            for key in dictionary:
                if key == key_to_check:
                    count += 1
                    if count > 1:
                        return True
            return False
    def forward(self, input_ids, **kwargs):
        for module in self:
            try:
                input = self.embedding(input_ids)
            except Exception as e:
                input = input_ids
                pass
            if "input_ids" in kwargs:
                kwargs.pop("input_ids", None)
            if isinstance(module, nn.Embedding):
                continue
            try:
                output = module(input_ids=input, **kwargs)
            except:
                output = module(input, **kwargs)
            try:
                input = output.last_hidden_state
            except:
                input = output[0]
            

        return output

class TextComprehensibilityLoss(nn.Module):
    def __init__(self, vocab_size, weight_similarity=1.0, weight_length=0.1, penalty_strength=0.1):
        super(TextComprehensibilityLoss, self).__init__()
        self.vocab_size = vocab_size
        self.weight_similarity = weight_similarity
        self.weight_length = weight_length
        self.penalty_strength = penalty_strength

    def forward(self, output, target):
        # Compute the similarity function (cosine similarity)
        cosine_similarity = torch.nn.functional.cosine_similarity(output, target.unsqueeze(1), dim=-1)

        # Compute the length penalty as the absolute difference in token lengths
        length_penalty = torch.abs(output.sum() - target.sum())

        # Normalize the similarity and length penalty terms
        normalized_similarity = (cosine_similarity + 1.0) / 2.0  # Normalize to [0, 1]
        normalized_length_penalty = length_penalty / self.vocab_size  # Normalize to [0, 1]

        # Compute the loss as a weighted combination of normalized similarity and length penalties
        loss = -torch.mean(
            normalized_similarity) * self.weight_similarity + normalized_length_penalty * self.weight_length

        # Add a penalty term to encourage the model to stay close to the target
        penalty = torch.mean(((output - target.unsqueeze(1)) ** 2) * self.penalty_strength) / self.vocab_size
        loss += penalty

        return loss
class FocusMechanism(nn.Module):
    """
    Implements a focus mechanism that directs the model's attention to specific parts
    of the input based on a learned focus vector. Unlike traditional attention mechanisms,
    this mechanism doesn't compute attention weights over the inputs but uses a focus
    vector to guide the model's focus.

    The focus mechanism is designed for scenarios where a subtask requires selective
    attention to particular portions of the input while ignoring non-critical information.
    The learned focus vector helps achieve this by emphasizing relevant information and
    suppressing irrelevant parts.

    Args:
        emb_dim (int): Embedding dimension of the input.
        hidden_dim (int): Size of the hidden representations.

    Inputs: 
        x (torch.Tensor): Input embeddings, shape (batch_size, seq_len, emb_dim).
        
    Outputs:
        focused_x (torch.Tensor): Input embeddings with focus weights applied, 
            shape (batch_size, seq_len, emb_dim).
        focus_vector (torch.Tensor): Learned focus vector that determines the relevance
            weights, shape (batch_size, hidden_dim).

    Example:
        # Create a FocusMechanism instance
        focus = FocusMechanism(emb_dim=64, hidden_dim=32)

        # Input tensor
        input_tensor = torch.randn(4, 10, 64)

        # Apply the focus mechanism
        focused_output, focus_vector = focus(input_tensor)
    """

    def __init__(self, emb_dim, hidden_dim):
        super().__init__()

        # Focus vector generator
        self.focus_generator = nn.Linear(emb_dim, hidden_dim)

        # Linear transformation
        self.linear = nn.Linear(emb_dim, hidden_dim)

        # Activation function
        self.tanh = nn.Tanh()

        # Softmax to compute focus weights
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        """
        Forward pass of the focus mechanism.

        Args:
            x (torch.Tensor): Input embeddings, shape (batch_size, seq_len, emb_dim).

        Returns:
            focused_x (torch.Tensor): Input embeddings with focus weights applied, 
                shape (batch_size, seq_len, emb_dim).
            focus_vector (torch.Tensor): Learned focus vector that determines the relevance
                weights, shape (batch_size, hidden_dim).
        """

        # Calculate the focus vector based on the mean of input embeddings
        focus_vector = self.focus_generator(x.mean(dim=0))

        # Calculate focus logits by applying focus_vector to input embeddings
        focus_logits = torch.sum(x * focus_vector, dim=-1)

        # Apply softmax to the logits to obtain focus weights
        focus_weights = self.softmax(focus_logits)

        # Expand dimensions for broadcasting
        focus_weights = focus_weights.unsqueeze(-1)

        # Apply focus weights to input embeddings
        focused_x = x * focus_weights

        return focused_x, focus_vector

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_seq_len=512):
        super(PositionalEncoding, self).__init__()

        # Compute the positional encodings once in log space
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x


class SENTIARMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-4):
        """
        LlamaRMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)


class SENTIARotaryEmbedding(torch.nn.Module):
    def __init__(self, dim, max_position_embeddings=2048, base=10000, device=None):
        super().__init__()

        self.dim = dim
        self.max_position_embeddings = max_position_embeddings
        self.base = base
        inv_freq = 1.0 / (self.base ** (torch.arange(0, self.dim, 2).float().to(device) / self.dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)

        # Build here to make `torch.jit.trace` work.
        self._set_cos_sin_cache(
            seq_len=max_position_embeddings, device=self.inv_freq.device, dtype=torch.get_default_dtype()
        )

    def _set_cos_sin_cache(self, seq_len, device, dtype):
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=device, dtype=self.inv_freq.dtype)

        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        # Different from paper, but it uses a different permutation in order to obtain the same calculation
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :].to(dtype), persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :].to(dtype), persistent=False)

    def forward(self, x, seq_len=None):
        # x: [bs, num_attention_heads, seq_len, head_size]
        if seq_len > self.max_seq_len_cached:
            self._set_cos_sin_cache(seq_len=seq_len, device=x.device, dtype=x.dtype)

        return (
            self.cos_cached[:, :, :seq_len, ...].to(dtype=x.dtype),
            self.sin_cached[:, :, :seq_len, ...].to(dtype=x.dtype),
        )


class SENTIALinearScalingRotaryEmbedding(SENTIARotaryEmbedding):
    """LlamaRotaryEmbedding extended with linear scaling. Credits to the Reddit user /u/kaiokendev"""

    def __init__(self, dim, max_position_embeddings=2048, base=10000, device=None, scaling_factor=1.0):
        self.scaling_factor = scaling_factor
        super().__init__(dim, max_position_embeddings, base, device)

    def _set_cos_sin_cache(self, seq_len, device, dtype):
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=device, dtype=self.inv_freq.dtype)
        t = t / self.scaling_factor

        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        # Different from paper, but it uses a different permutation in order to obtain the same calculation
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :].to(dtype), persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :].to(dtype), persistent=False)


class SENTIADynamicNTKScalingRotaryEmbedding(SENTIARotaryEmbedding):
    """LlamaRotaryEmbedding extended with Dynamic NTK scaling. Credits to the Reddit users /u/bloc97 and /u/emozilla"""

    def __init__(self, dim, max_position_embeddings=2048, base=10000, device=None, scaling_factor=1.0):
        self.scaling_factor = scaling_factor
        super().__init__(dim, max_position_embeddings, base, device)

    def _set_cos_sin_cache(self, seq_len, device, dtype):
        self.max_seq_len_cached = seq_len

        if seq_len > self.max_position_embeddings:
            base = self.base * (
                    (self.scaling_factor * seq_len / self.max_position_embeddings) - (self.scaling_factor - 1)
            ) ** (self.dim / (self.dim - 2))
            inv_freq = 1.0 / (base ** (torch.arange(0, self.dim, 2).float().to(device) / self.dim))
            self.register_buffer("inv_freq", inv_freq, persistent=False)

        t = torch.arange(self.max_seq_len_cached, device=device, dtype=self.inv_freq.dtype)

        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        # Different from paper, but it uses a different permutation in order to obtain the same calculation
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :].to(dtype), persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :].to(dtype), persistent=False)


def rotate_half(x):
    """Rotates half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2:]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(q, k, cos, sin, position_ids):
    # The first two dimensions of cos and sin are always 1, so we can `squeeze` them.
    cos = cos.squeeze(1).squeeze(0)  # [seq_len, dim]
    sin = sin.squeeze(1).squeeze(0)  # [seq_len, dim]
    cos = cos[position_ids].unsqueeze(1)  # [bs, 1, seq_len, dim]
    sin = sin[position_ids].unsqueeze(1)  # [bs, 1, seq_len, dim]
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


class SENTIAMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = ACT2FN[config.hidden_act]

    def forward(self, x):
        if self.config.pretraining_tp > 1:
            slice = self.intermediate_size // self.config.pretraining_tp
            gate_proj_slices = self.gate_proj.weight.split(slice, dim=0)
            up_proj_slices = self.up_proj.weight.split(slice, dim=0)
            down_proj_slices = self.down_proj.weight.split(slice, dim=1)

            gate_proj = torch.cat(
                [F.linear(x, gate_proj_slices[i]) for i in range(self.config.pretraining_tp)], dim=-1
            )
            up_proj = torch.cat([F.linear(x, up_proj_slices[i]) for i in range(self.config.pretraining_tp)], dim=-1)

            intermediate_states = (self.act_fn(gate_proj) * up_proj).split(slice, dim=2)
            down_proj = [
                F.linear(intermediate_states[i], down_proj_slices[i]) for i in range(self.config.pretraining_tp)
            ]
            down_proj = sum(down_proj)
        else:
            down_proj = self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))

        return down_proj


def repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    """
    This is the equivalent of torch.repeat_interleave(x, dim=1, repeats=n_rep). The hidden states go from (batch,
    num_key_value_heads, seqlen, head_dim) to (batch, num_attention_heads, seqlen, head_dim)
    """
    batch, num_key_value_heads, slen, head_dim = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    hidden_states = hidden_states[:, :, None, :, :].expand(batch, num_key_value_heads, n_rep, slen, head_dim)
    return hidden_states.reshape(batch, num_key_value_heads * n_rep, slen, head_dim)


class SENTIAAttention(nn.Module):
    """Multi-headed attention from 'Attention Is All You Need' paper"""

    def __init__(self, config: SENTIAConfig, cross_attention=False):
        super().__init__()
        self.config = config
        self.cross_attention = cross_attention
        self.hidden_size = config.hidden_dim
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        self.num_key_value_heads = config.num_key_value_heads
        self.num_key_value_groups = self.num_heads // self.num_key_value_heads
        self.max_position_embeddings = config.max_position_embeddings

        if (self.head_dim * self.num_heads) != self.hidden_size:
            raise ValueError(
                f"hidden_size must be divisible by num_heads (got `hidden_size`: {self.hidden_size}"
                f" and `num_heads`: {self.num_heads})."
            )
        self.q_proj = nn.Linear(self.hidden_size, self.num_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(self.hidden_size, self.num_key_value_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(self.hidden_size, self.num_key_value_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(self.num_heads * self.head_dim, self.hidden_size, bias=False)
        self._init_rope()

    def _init_rope(self):
        if self.config.rope_scaling is None:
            self.rotary_emb = SENTIARotaryEmbedding(self.head_dim, max_position_embeddings=self.max_position_embeddings)
        else:
            scaling_type = self.config.rope_scaling["type"]
            scaling_factor = self.config.rope_scaling["factor"]
            if scaling_type == "linear":
                self.rotary_emb = SENTIALinearScalingRotaryEmbedding(
                    self.head_dim, max_position_embeddings=self.max_position_embeddings, scaling_factor=scaling_factor
                )
            elif scaling_type == "dynamic":
                self.rotary_emb = SENTIADynamicNTKScalingRotaryEmbedding(
                    self.head_dim, max_position_embeddings=self.max_position_embeddings, scaling_factor=scaling_factor
                )
            else:
                raise ValueError(f"Unknown RoPE scaling type {scaling_type}")

    def _shape(self, tensor: torch.Tensor, seq_len: int, bsz: int):
        return tensor.view(bsz, seq_len, self.num_heads, self.head_dim).transpose(1, 2).contiguous()

    def forward(
            self,
            hidden_states: torch.Tensor,
            attention_mask: Optional[torch.Tensor] = None,
            encoder_states: Optional[torch.tensor] = None,
            encoder_attention_mask: Optional[torch.tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_value: Optional[Tuple[torch.Tensor]] = None,
            output_attentions: bool = False,
            use_cache: bool = False,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()
        encoder_mask = encoder_attention_mask  # im lazy (for context I made a mistake somewhere)

        if self.config.pretraining_tp > 1:
            if not self.cross_attention:
                key_value_slicing = (self.num_key_value_heads * self.head_dim) // self.config.pretraining_tp
                query_slices = self.q_proj.weight.split(
                    (self.num_heads * self.head_dim) // self.config.pretraining_tp, dim=0
                )
                key_slices = self.k_proj.weight.split(key_value_slicing, dim=0)
                value_slices = self.v_proj.weight.split(key_value_slicing, dim=0)

                query_states = [F.linear(hidden_states, query_slices[i]) for i in range(self.config.pretraining_tp)]
                query_states = torch.cat(query_states, dim=-1)

                key_states = [F.linear(hidden_states, key_slices[i]) for i in range(self.config.pretraining_tp)]
                key_states = torch.cat(key_states, dim=-1)

                value_states = [F.linear(hidden_states, value_slices[i]) for i in range(self.config.pretraining_tp)]
                value_states = torch.cat(value_states, dim=-1)
            else:
                key_value_slicing = (self.num_key_value_heads * self.head_dim) // self.config.pretraining_tp
                query_slices = self.q_proj.weight.split(
                    (self.num_heads * self.head_dim) // self.config.pretraining_tp, dim=0
                )
                key_slices = self.k_proj.weight.split(key_value_slicing, dim=0)
                value_slices = self.v_proj.weight.split(key_value_slicing, dim=0)

                query_states = [F.linear(hidden_states, query_slices[i]) for i in range(self.config.pretraining_tp)]
                query_states = torch.cat(query_states, dim=-1)

                key_states = [F.linear(encoder_states, key_slices[i]) for i in range(self.config.pretraining_tp)]
                key_states = torch.cat(key_states, dim=-1)

                value_states = [F.linear(encoder_states, value_slices[i]) for i in range(self.config.pretraining_tp)]
                value_states = torch.cat(value_states, dim=-1)

        else:
            if not self.cross_attention:
                query_states = self.q_proj(hidden_states)
                key_states = self.k_proj(hidden_states)
                value_states = self.v_proj(hidden_states)
            else:
                query_states = self.q_proj(hidden_states)
                key_states = self.k_proj(encoder_states)
                value_states = self.v_proj(encoder_states)
        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            kv_seq_len += past_key_value[0].shape[-2]
        cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, position_ids)

        if past_key_value is not None:
            # reuse k, v, self_attention
            key_states = torch.cat([past_key_value[0], key_states], dim=2)
            value_states = torch.cat([past_key_value[1], value_states], dim=2)

        past_key_value = (key_states, value_states) if use_cache else None

        # repeat k/v heads if n_kv_heads < n_heads
        key_states = repeat_kv(key_states, self.num_key_value_groups)
        value_states = repeat_kv(value_states, self.num_key_value_groups)

        attn_weights = torch.matmul(query_states, key_states.transpose(2, 3)) / math.sqrt(self.head_dim)

        if attn_weights.size() != (bsz, self.num_heads, q_len, kv_seq_len):
            raise ValueError(
                f"Attention weights should be of size {(bsz, self.num_heads, q_len, kv_seq_len)}, but is"
                f" {attn_weights.size()}"
            )

        if attention_mask is not None:
            if attention_mask.size() != (bsz, 1, q_len, kv_seq_len):
                raise ValueError(
                    f"Attention mask should be of size {(bsz, 1, q_len, kv_seq_len)}, but is {attention_mask.size()}"
                )
            attn_weights = attn_weights + attention_mask
        if encoder_mask is not None:
            if encoder_mask.size() != (bsz, 1, q_len, kv_seq_len):
                encoder_mask = None
            attn_weights = attn_weights + encoder_mask

        # upcast attention to fp32
        attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
        attn_output = torch.matmul(attn_weights, value_states)

        if attn_output.size() != (bsz, self.num_heads, q_len, self.head_dim):
            raise ValueError(
                f"`attn_output` should be of size {(bsz, self.num_heads, q_len, self.head_dim)}, but is"
                f" {attn_output.size()}"
            )

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)

        if self.config.pretraining_tp > 1:
            attn_output = attn_output.split(self.hidden_size // self.config.pretraining_tp, dim=2)
            o_proj_slices = self.o_proj.weight.split(self.hidden_size // self.config.pretraining_tp, dim=1)
            attn_output = sum([F.linear(attn_output[i], o_proj_slices[i]) for i in range(self.config.pretraining_tp)])
        else:
            attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, past_key_value


class SENTIAEncoderLayer(nn.Module):
    def __init__(self, config: SENTIAConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.is_cross_attention = config.add_cross_attention
        self.self_attn = SENTIAAttention(config=config)
        self.mlp = SENTIAMLP(config)
        self.input_layernorm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(
            self,
            input_ids: torch.Tensor,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_value: Optional[Tuple[torch.Tensor]] = None,
            output_attentions: Optional[bool] = True,
            use_cache: Optional[bool] = False,
            return_dict: Optional[bool] = True,
            output_hidden_states: Optional[bool] = None,

    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        """
        Args:
            hidden_states (`torch.FloatTensor`): input to the layer of shape `(batch, seq_len, embed_dim)`
            attention_mask (`torch.FloatTensor`, *optional*): attention mask of size
                `(batch, 1, tgt_len, src_len)` where padding elements are indicated by very large negative values.
            output_attentions (`bool`, *optional*):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more detail.
            use_cache (`bool`, *optional*):
                If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding
                (see `past_key_values`).
            past_key_value (`Tuple(torch.FloatTensor)`, *optional*): cached past key and value projection states
        """
        hidden_states = input_ids
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)

        # Self Attention
        attn, self_attn_weights, present_key_value = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            use_cache=use_cache,
        )
        hidden_states = residual + attn

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states
        if hidden_states.dtype == torch.float16 and (
                torch.isinf(hidden_states).any() or torch.isnan(hidden_states).any()
        ):
            clamp_value = torch.finfo(hidden_states.dtype).max - 1000
            hidden_states = torch.clamp(hidden_states, min=-clamp_value, max=clamp_value)

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weights,)

        if use_cache:
            outputs += (present_key_value,)

        if not return_dict:
            return outputs, attn
        else:
            return BaseModelOutputWithPast(
                last_hidden_state=hidden_states,
                past_key_values=past_key_value,
                hidden_states=outputs,
                attentions=attn,
            )


class SENTIADecoderLayer(nn.Module):
    def __init__(self, config: SENTIAConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.is_cross_attention = config.add_cross_attention
        self.focus = FocusMechanism(config.hidden_dim, config.hidden_dim)
        if self.is_cross_attention:
            self.cross_attention = SENTIAAttention(config, cross_attention=True)
        self.self_attn = SENTIAAttention(config=config)
        self.mlp = SENTIAMLP(config)
        self.input_layernorm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(
            self,
            input_ids: torch.Tensor,
            decoder_attention_mask: Optional[torch.Tensor] = None,
            encoder_hidden_states: Optional[torch.Tensor] = None,
            encoder_attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_value: Optional[Tuple[torch.Tensor]] = None,
            output_attentions: Optional[bool] = True,
            use_cache: Optional[bool] = False,
            return_dict: Optional[bool] = True,
            output_hidden_states: Optional[bool] = None,
    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        """
        Args:
            hidden_states (`torch.FloatTensor`): input to the layer of shape `(batch, seq_len, embed_dim)`
            attention_mask (`torch.FloatTensor`, *optional*): attention mask of size
                `(batch, 1, tgt_len, src_len)` where padding elements are indicated by very large negative values.
            output_attentions (`bool`, *optional*):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more detail.
            use_cache (`bool`, *optional*):
                If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding
                (see `past_key_values`).
            past_key_value (`Tuple(torch.FloatTensor)`, *optional*): cached past key and value projection states
        """
        hidden_states = input_ids
        if hidden_states is None:
            hidden_states = encoder_hidden_states
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        residual = hidden_states
        focus, _ = self.focus(hidden_states)
        hidden_states = residual + focus
        residual = hidden_states
        # Self Attention
        attn, self_attn_weights, present_key_value = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=decoder_attention_mask,
            position_ids=position_ids,
            past_key_value=None,
            output_attentions=output_attentions,
            use_cache=use_cache,
        )
        hidden_states = residual + attn
        cross_attn_weights = self_attn_weights
        # Cross Attention
        if self.is_cross_attention:
            residual = hidden_states

            hidden_states, cross_attn_weights, present_key_value = self.cross_attention(
                hidden_states=hidden_states,
                attention_mask=None, # No attention mask for cross attention
                encoder_attention_mask=encoder_attention_mask,
                encoder_states=encoder_hidden_states,
                position_ids=position_ids,
                past_key_value=None,
                output_attentions=output_attentions,
                use_cache=use_cache,
            )
            hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states
        if hidden_states.dtype == torch.float16 and (
                torch.isinf(hidden_states).any() or torch.isnan(hidden_states).any()
        ):
            clamp_value = torch.finfo(hidden_states.dtype).max - 1000
            hidden_states = torch.clamp(hidden_states, min=-clamp_value, max=clamp_value)

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weights,)

        if use_cache:
            outputs += (present_key_value,)
        if not return_dict:
            return outputs, attn
        else:
            return BaseModelOutputWithPastAndCrossAttentions(
                last_hidden_state=hidden_states,
                past_key_values=past_key_value,       
                hidden_states=outputs,
                attentions=self_attn_weights,
                cross_attentions=cross_attn_weights
            )


LLAMA_START_DOCSTRING = r"""
    This model inherits from [`PreTrainedModel`]. Check the superclass documentation for the generic methods the
    library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
    etc.)

    This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
    Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
    and behavior.

    Parameters:
        config ([`LlamaConfig`]):
            Model configuration class with all the parameters of the model. Initializing with a config file does not
            load the weights associated with the model, only the configuration. Check out the
            [`~PreTrainedModel.from_pretrained`] method to load the model weights.
"""


@add_start_docstrings(
    "The bare LLaMA Model outputting raw hidden-states without any specific head on top.",
    LLAMA_START_DOCSTRING,
)
class SENTIAPreTrainedModel(PreTrainedModel):
    config_class = SENTIAConfig
    base_model_prefix = "model"
    supports_gradient_checkpointing = True
    _no_split_modules = ["SENTIADecoderLayer"]
    _skip_keys_device_placement = "past_key_values"

    def _init_weights(self, module):
        std = self.config.initializer_range
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()

    def _set_gradient_checkpointing(self, module, value=False):
        if isinstance(module, SENTIADecoderModel):
            module.gradient_checkpointing = value

    def _shift_right(self, input_ids):
        decoder_start_token_id = self.config.decoder_start_token_id
        pad_token_id = self.config.pad_token_id

        if decoder_start_token_id is None:
            raise ValueError(
                "self.model.config.decoder_start_token_id has to be defined. In sentia it is usually set to the "
                "pad_token_id."
                "See sentia docs for more information."
            )

        # shift inputs to the right
        if is_torch_fx_proxy(input_ids):
            # Item assignment is not supported natively for proxies.
            shifted_input_ids = torch.full(input_ids.shape[:-1] + (1,), decoder_start_token_id)
            shifted_input_ids = torch.cat([shifted_input_ids, input_ids[..., :-1]], dim=-1)
        else:
            shifted_input_ids = input_ids.new_zeros(input_ids.shape)
            shifted_input_ids[..., 1:] = input_ids[..., :-1].clone()
            shifted_input_ids[..., 0] = decoder_start_token_id

        if pad_token_id is None:
            raise ValueError("self.model.config.pad_token_id has to be defined.")
        # replace possible -100 values in labels by `pad_token_id`
        shifted_input_ids.masked_fill_(shifted_input_ids == -100, pad_token_id)

        return shifted_input_ids

    def backward(self, loss, threshold=1e-6):
        """
        Backward pass of the SENTIA model with optional gradient pruning.

        Args:
            loss (torch.Tensor): Loss tensor.
            threshold (float, optional): Threshold value for gradient pruning. Defaults to 1e-6.
        """
        for p in self.parameters():
            if p.grad is not None and torch.max(torch.abs(p.grad)) < threshold:
                p.grad = None
        loss.backward()

    def save(self, directory):
        """
        Save the SENTIA model to a given directory.

        Args:
            model (nn.Module): The SENTIA model instance to save.
            directory (str): The directory path to save the model.

        Returns:
            None
        """
        model = self
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the model's state dictionary
        model_path = os.path.join(directory, 'pytorch_model.bin')
        torch.save(model.state_dict(), model_path)

        print(f"Model saved at {model_path}")

    def load(self, directory):
        """
        Load the SENTIA model from a given directory.

        Args:
            model_class (nn.Module): The class of the SENTIA model to instantiate.
            directory (str): The directory path where the model is saved.

        Returns:
            model (nn.Module): The loaded SENTIA model.
        """
        # Instantiate the model
        model = self

        # Load the saved model's state dictionary
        try:
            model_path = os.path.join(directory, 'sentia_model.bin')
            model.load_state_dict(torch.load(model_path), strict=False)
        except Exception:
            model_path = os.path.join(directory, 'pytorch_model.bin')
            model.load_state_dict(torch.load(model_path), strict=False)

        print(f"Model loaded from {model_path}")

        return model

    @staticmethod
    def keytoken_weighted_loss(logits, inputs, keytoken_ids, alpha=1.0):
        # Calculate per-token loss
        loss_fct = nn.CrossEntropyLoss(reduce=False)
        loss = loss_fct(logits.view(-1, logits.size(-1)), inputs.view(-1))
        # Resize and average loss per sample
        loss_per_sample = loss.mean()
        # Calculate and scale weighting
        weights = torch.stack([(inputs == kt).float() for kt in keytoken_ids]).sum()
        weights = alpha * (1.0 + weights)
        # Calculate weighted average
        weighted_loss = (loss_per_sample * weights).mean()
        return weighted_loss

    def _generate(
            self,
            input_ids,
            temperature=0.6,
            top_k=50,
            top_p=0.92,
            max_length=20,
            repetition_penalty=1.176,
            device="cuda" if torch.cuda.is_available() else "cpu"
    ):
        warnings.warn("This method is deprecated, please use generate() instead")
        model = self
        model.eval()
        input_ids = input_ids.to(device)
        generated_text = input_ids.clone()  # Initialize with the provided input_ids

        for step in range(max_length):
            logits = model.forward(generated_text).logits  # Generate logits for the current input

            # Keep only the last token predictions of the first batch item (batch size 1), apply a temperature
            # coefficient and filter
            logits = logits[0, -1, :] / temperature
            filtered_logits = self.top_k_top_p_filtering(logits, top_k=top_k, top_p=top_p)

            # Apply a minimum threshold for top-k filtering
            filtered_logits = self.apply_min_threshold(filtered_logits, min_threshold=0.1)

            # Apply repetition penalty to the logits
            if step > 0:
                for prev_token in generated_text[0]:
                    filtered_logits[prev_token] /= repetition_penalty

            # Sample the next token using multinomial distribution
            next_token_probs = F.softmax(filtered_logits, dim=-1)
            next_token_index = torch.multinomial(next_token_probs, 1)
            next_token = next_token_index.squeeze()

            # Append the next token to the generated text
            generated_text = torch.cat((generated_text, next_token.unsqueeze(0).unsqueeze(0)), dim=1)

            # Stop generating if the generated text reaches the desired max_length
            if generated_text.size(1) >= max_length:
                break

        return generated_text

    def _reorder_past(self, past, next_tokens):
        """
        Reorders the past state based on the selected next tokens.

        Args:
            past (tuple): Tuple containing the past states.
            next_tokens (torch.Tensor): Tensor containing the selected next tokens of shape (batch_size * num_beams).

        Returns:
            tuple: Reordered past state.
        """
        next_tokens = next_tokens.unsqueeze(-1).unsqueeze(-1)
        past = tuple([p.index_select(1, next_tokens[i].view(-1)) for i, p in enumerate(past)])
        return past

    @staticmethod
    def calculate_accuracy(predictions, targets):
        """
        Calculate the accuracy.

        Args:
            predictions (Tensor): Model predictions (e.g., logits).
            targets (Tensor): Ground truth labels.

        Returns:
            float: Accuracy.
        """
        predicted_classes = predictions
        correct_predictions = torch.sum(predicted_classes == targets).item()
        total_predictions = targets.size(0)  # Number of samples

        accuracy = correct_predictions / total_predictions
        return accuracy

    @staticmethod
    def apply_min_threshold(logits, min_threshold=0.1):
        # Apply a minimum threshold to logits to prevent very small values
        logits = torch.max(logits, torch.tensor(min_threshold).to(logits.device))
        return logits

    @staticmethod
    def nucleus_sampling(logits):
        # Perform nucleus sampling based on the logits
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Find the smallest index whose cumulative probability exceeds a threshold (0.95)
        nucleus_indices = cumulative_probs <= 0.95

        # Select the next token from nucleus sampling
        selected_index = torch.randint(0, nucleus_indices.size(1), (1,))
        next_token = sorted_indices[0, selected_index]

        return next_token

    @staticmethod
    def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
        """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
            Args:
                logits: logits distribution shape (vocabulary size)
                top_k >0: keep only top k tokens with highest probability (top-k filtering).
                top_p >0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                    Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        """
        logits = logits.squeeze(0)
        top_k = min(top_k, logits.size(-1))  # Safety check
        if top_k > 0:
            # Remove all tokens with a probability less than the last token of the top-k
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probs > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value
        return logits

    # Will most likely will be deprecated in the future, you can create your own training loop, or use Trainer.
    @staticmethod
    def fit(model, num_epochs, dataloader, tokenizer, optimizer, val_dataloader, scheduler, device: torch.device,
            lr=4e-4):
        def lr_lambda(current_step):
            if current_step < 3000:
                return current_step / 3000
            return max(
                0.1,
                (num_epochs * len(dataloader) - current_step) / (num_epochs * len(dataloader) - 1500)
            )

        """
        Train the SENTIA model.

        Args:
            num_epochs (int): Number of training epochs.
            dataloader (DataLoader): Training data loader.
            model: The SENTIA model instance.
            tokenizer: Tokenizer for decoding predictions.
            optimizer: Optimizer for model parameter updates.
            val_dataloader (DataLoader): Validation data loader.
            scheduler: Learning rate scheduler.
        """
        keytoken_ids = []
        for keyword in [
            "plt",
            "pd",
            "sk",
            "fit",
            "predict",
            " plt",
            " pd",
            " sk",
            " fit",
            " predict",
            "testtest",
        ]:
            ids = tokenizer([keyword]).input_ids[0]
            if len(ids) == 1:
                keytoken_ids.append(ids[0])
            else:
                print(f"Keyword has not single token: {keyword}")
        optimizer = optimizer(model.parameters(), lr, eps=1e-4, fused=True)
        scheduler = scheduler(optimizer, lr_lambda=lr_lambda)
        scaler = torch.cuda.amp.grad_scaler.GradScaler()
        for epoch in range(num_epochs):
            model.train()
            print(f"Epoch {epoch + 1}/{num_epochs}")
            total_loss = 0
            total_reward = 0
            total_bleu = 0
            total_perplexity = 0
            num_batches = 0
            accumulation_steps = 12  # Accumulate gradients over 12 batches
            predictions_list: list = []
            bleu_scores: list = []
            for i, batch in tqdm(enumerate(dataloader)):
                input_ids = batch["input_ids"].to(device)
                target_ids = batch["labels"].to(device)
                target_text = batch["target_text"]
                # Generate the output and calculate the loss
                outputs = model(input_ids=input_ids, labels=target_ids)
                loss, logits = outputs[:2]
                # loss = torch.exp(loss)
                # Calculate the BLEU score
                # probs = F.softmax(logits, dim=-1)
                predictions = torch.argmax(logits, dim=-1)
                predictions_str = [tokenizer.decode(pred, skip_special_tokens=True) for pred in predictions.tolist()]
                target_ids_str = [tokenizer.decode(tgt, skip_special_tokens=True) for tgt in target_ids.tolist()]
                print(predictions_str[0])
                bleu_scores = []
                accuracy_scores = []
                for pred_str, target_str in zip(predictions_str, target_ids_str):
                    bleu = sacrebleu.sentence_bleu(pred_str, [target_str])
                    bleu_scores.append(bleu.score)
                for pred_id, target_id in zip(predictions, target_ids):
                    accuracy = SENTIADecoderModel.calculate_accuracy(pred_id, target_id)
                    accuracy_scores.append(accuracy)

                accuracy = sum(accuracy_scores) / len(accuracy_scores)
                bleu = sum(bleu_scores) / len(bleu_scores)
                # Calculate the reward
                reward, penalty = SENTIADecoderModel.get_reward(predictions.tolist()[0], target_ids.tolist()[0], bleu)
                ol = loss
                # loss = torch.exp(loss) # Shown to drastically improve model performance
                # Backpropagate the loss and update the parameters with the reward
                # if penalty > 0 and penalty > reward:
                # loss = (loss * ((penalty - reward) * 5))
                # if reward > penalty:
                # loss = (loss / ((reward - penalty) * 5))
                # if torch.isnan(loss):
                # print("Skipped non-finite loss")
                # print(loss.item())
                # model.save_pretrained('D:\\Projects\\exploded\\')
                # quit(0)
                loss.backward()
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                # Update the metrics
                total_loss += loss.item()
                # total_reward += reward
                total_bleu += bleu
                total_perplexity += torch.exp(ol).item()
                num_batches += 1
                #wandb.log({"loss": ol.item(), "bleu": bleu, "perplexity": torch.exp(ol).item(), "accuracy": accuracy})
                print(
                    f"Epoch {epoch + 1}/{num_epochs}, Batch {i + 1}/{len(dataloader)}: Loss - {ol.item():.4f}, NetReward - {reward - penalty:.4f}, BLEU - {bleu:.4f}, Perplexity - {torch.exp(ol).item()}, Accuracy - {accuracy}")
            # Display the metrics for the epoch
            model = model.get_base_model()
            model.save(r'D:\Projects\chatTulu')
            tokenizer.save_pretrained(r'D:\Projects\chatTulu')
            # val_loss, val_reward, val_penalty, val_bleu, val_perplexity, val_accuracy = SENTIADecoderModel.evaluate(model, val_dataloader, tokenizer, device)
            # wandb.log({"val_loss": val_loss.item(), "val_bleu": val_bleu, "val_perplexity": val_perplexity, "val_accuracy": val_accuracy,})
            # print(f"Validation metrics: Loss={val_loss:.4f}, Reward={reward-penalty:.4f}, BLEU={val_bleu:.4f}, Perplexity={val_perplexity:.4f}")

    @staticmethod
    def get_reward(predictions, target_ids, bleu_score, bleu_threshold=5):
        """
        Calculate the reward and penalty for the generated predictions.

        Args:
            predictions (list): List of predicted output tokens.
            target_ids (list): List of target output tokens.
            bleu_threshold (float): Threshold for BLEU score reward.
            perplexity_threshold (float): Threshold for perplexity penalty.

        Returns:
            reward (float): Reward score.
            penalty (float): Penalty score.
        """
        reward = 0
        penalty = 0

        # Calculate BLEU score
        # Check each prediction against its corresponding target ID
        for i in range(len(predictions)):
            # Reward for BLEU score higher than the threshold
            if bleu_score > bleu_threshold:
                reward += 1
            # Penalize for BLEU score lower than 1 by dividing the penalty
            if bleu_score < 1:
                penalty += 1 / (bleu_score + 1)
            if predictions[i] == "[PAD]":
                penalty += 1
            if predictions[i] != "[PAD]":
                reward += 1
            # Penalize for repeating words consecutively
            if i > 0 and predictions[i] == predictions[i - 1]:
                penalty += 1
            # Reward for using words correctly at the same index
            if i < len(target_ids) and predictions[i] == target_ids[i]:
                reward += 1
            elif predictions[i] in target_ids:
                reward += 0.25

        return reward, penalty

    @staticmethod
    def evaluate(model, dataloader, tokenizer, device: torch.device):
        """
        Evaluate the model on the validation set and calculate metrics.

        Args:
            model (nn.Module): Model to evaluate.
            dataloader (DataLoader): Validation data loader.
            tokenizer: Tokenizer for decoding predictions.

        Returns:
            avg_loss (float): Average loss.
            avg_reward (float): Average reward.
            avg_penalty (float): Average penalty.
            avg_bleu (float): Average BLEU score.
            avg_perplexity (float): Average perplexity.
        """
        model.eval()
        total_loss = 0
        total_reward = 0
        total_bleu = 0
        total_perplexity = 0
        num_batches = 0
        total_penalty = 0
        total_accuracy = 0

        with torch.no_grad():
            for batch in dataloader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                target_ids = batch["labels"].to(device)
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                target_ids = target_ids.to(device)
                target_text = batch["target_text"]
                # Generate the output and calculate the loss
                outputs = model(inputs_ids=input_ids, labels=target_ids)
                loss, logits = outputs[:2]
                # Calculate the BLEU score
                predictions = torch.argmax(logits, dim=-1)
                predictions_str = [tokenizer.decode(pred, skip_special_tokens=True) for pred in predictions.tolist()]
                target_str = [tokenizer.decode(tgt, skip_special_tokens=True) for tgt in target_ids.tolist()]
                bleu_scores = []
                accuracy_scores = []
                for pred_str, target_str in zip(predictions_str, target_str):
                    bleu = sacrebleu.sentence_bleu(pred_str, [target_str])
                    bleu_scores.append(bleu.score)
                for pred_id, target_id in zip(predictions_str, target_str):
                    SENTIAPreTrainedModel.calculate_accuracy(target_id, pred_id)
                    accuracy_scores.append(accuracy)
                accuracy = sum(accuracy_scores) / len(accuracy_scores)
                bleu = sum(bleu_scores) / len(bleu_scores)
                reward, penalty = SENTIADecoderModel.get_reward(predictions_str[0], target_str[0], bleu)
                # Update the metrics
                total_loss += loss
                total_reward += reward
                total_penalty += penalty
                total_bleu += bleu
                total_accuracy += accuracy
                total_perplexity += torch.exp(torch.tensor(loss)).item()
                num_batches += 1

        # Calculate the average metrics
        avg_loss = total_loss / num_batches
        avg_reward = total_reward / num_batches
        avg_bleu = total_bleu / num_batches
        avg_perplexity = total_perplexity / num_batches
        avg_penalty = total_penalty / num_batches
        avg_accuracy = total_accuracy / num_batches
        return avg_loss, avg_reward, avg_penalty, avg_bleu, avg_perplexity, avg_accuracy

    def summary(self):
        """
        Print a summary of the model architecture and the number of parameters.
        """
        model = self
        num_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

        print("Model Summary:")
        print(f"{'=' * 40}")
        print(model)
        print(f"{'=' * 40}")
        print(f"Total params: {num_params}")
        print(f"Trainable params: {trainable_params}")


class MEPA(nn.Module):
    """
    Mutation Enhanced Plasticity Architecture (MEPA) Module with multiple layers.

    This module implements a fully connected layer, also known as a Multi-Layer Perceptron (MLP),
    with an affine transformation. It takes an input tensor and applies a linear transformation
    followed by bias addition. The weights and biases of the module are learned during training.

    Args:
        hidden_dim (int): The size of the input and output features.
        layers (int): The number of layers in the network.
        activation (callable, optional): The activation function to be applied after forwarding
            through all layers. Default is F.sigmoid

    Shape:
        - Input: `(batch_size, hidden_dim)` or `(batch_size, *, hidden_dim)` where `*` represents
          any number of additional dimensions.
        - Output: `(batch_size, hidden_dim)` or `(batch_size, *, hidden_dim)` depending on the
          input shape.

    Example:
        >>> hidden_dim = 10
        >>> batch_size = 32
        >>> input_tensor = torch.randn(batch_size, hidden_dim)
        >>> layers = 3
        >>> mepa = MEPA(hidden_dim, layers)
        >>> output_tensor = mepa(input_tensor)
        >>> print(output_tensor.shape)
        torch.Size([32, 10])
    """

    class MEPALayer(nn.Module):
        """
        A single layer of the Mutation Enhanced Plasticity Architecture (MEPA) module.

        Args:
            hidden_dim (int): The size of the input and output features for this layer.

        Shape:
            - Input: `(batch_size, hidden_dim)`
            - Output: `(batch_size, hidden_dim)`
        """

        def __init__(self, config: SENTIAConfig):
            super(MEPA.MEPALayer, self).__init__()
            self.config = config
            self.hidden_dim = config.hidden_dim
            hidden_dim = config.hidden_dim
            # self.weight = nn.Linear(hidden_dim, hidden_dim)
            from transformers.pytorch_utils import Conv1D
            self.scaling_matrix = Conv1D(hidden_dim, hidden_dim)
            self.memory = nn.LSTM(hidden_dim, hidden_dim)
            self.layer_norm = SENTIARMSNorm(hidden_dim)
            self.rms = SENTIARMSNorm(hidden_dim)
            self.ffn = SENTIAMLP(config)
            self.reset_parameters()
        def reset_parameters(self):
            """
            Initialize the layer's parameters.

            This function initializes the weight, bias, and scaling matrix parameters of the layer
            using Kaiming normal initialization for the weight, and uniform initialization for
            bias and scaling matrix.

            Shape:
                - weight: `(hidden_dim, hidden_dim)`
                - bias: `(hidden_dim)`
                - scaling_matrix: `(hidden_dim, hidden_dim)`
            """
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.scaling_matrix.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.scaling_matrix.bias, -bound, bound)
            nn.init.xavier_normal_(self.scaling_matrix.weight, bound)

        def forward(self, x):
            """
            Forward pass of the MEPALayer.

            Args:
                x (torch.Tensor): The input tensor of shape `(batch_size, hidden_dim)`.

            Returns:
                torch.Tensor: The output tensor of shape `(batch_size, hidden_dim)`.
            """
            x = self._shift_right(x)
            x, _ = self.memory(x)
            scaled = self.layer_norm((self.scaling_matrix(x) + x)) / 0.361
            scaled = F.softmax(scaled, dim=-1, dtype=x.dtype)
            ffn_out = self.ffn(scaled)
            return self.rms(ffn_out + scaled)

        def _shift_right(self, input_ids):
            decoder_start_token_id = self.config.decoder_start_token_id
            pad_token_id = self.config.pad_token_id

            if decoder_start_token_id is None:
                raise ValueError(
                    "self.model.config.decoder_start_token_id has to be defined. In SENTIA it is usually set to the pad_token_id."
                )
            shifted_input_ids = input_ids.new_zeros(input_ids.shape)
            shifted_input_ids[..., 1:] = input_ids[..., :-1].clone()
            shifted_input_ids[..., 0] = decoder_start_token_id

            if pad_token_id is None:
                raise ValueError("self.model.config.pad_token_id has to be defined.")
            # replace possible -100 values in labels by `pad_token_id`
            shifted_input_ids.masked_fill_(shifted_input_ids == -100, pad_token_id)

            return shifted_input_ids

    def __init__(self, config: SENTIAConfig):
        """
        Initialize the Mutation Enhanced Plasticity Architecture (MEPA) module.

        Args:
            config (SENTIAConfig): Configuration from the SENTIA model to intialize MEPA.
        """
        super().__init__()
        self.activation = None
        self.hidden_dim = config.hidden_dim
        self.layers = config.n_layer
        self.layer_modules = nn.ModuleList([self.MEPALayer(config) for _ in range(self.layers)])
    def forward(self, x):
        """
        Forward pass of the MEPA module.

        Args:
            x (torch.Tensor): The input tensor of shape `(batch_size, hidden_dim)` or
                `(batch_size, *, hidden_dim)`.

        Returns:
            torch.Tensor: The output tensor of shape `(batch_size, hidden_dim)` or
                `(batch_size, *, hidden_dim)` depending on the input shape.
        """
        if x.dim() > 2:
            x = x.reshape(x.size(0), x.size(1), -1)

        for layer_module in self.layer_modules:
            # Apply the current layer's transformation
            hidden_states = layer_module(x)
        if hidden_states.dtype == torch.float16 and (
                torch.isinf(hidden_states).any() or torch.isnan(hidden_states).any()):
            clamp_value = torch.finfo(hidden_states.dtype).max - 1000
            hidden_states = torch.clamp(hidden_states, min=-clamp_value, max=clamp_value)

        return hidden_states


LLAMA_INPUTS_DOCSTRING = r"""
    Args:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            Indices of input sequence tokens in the vocabulary. Padding will be ignored by default should you provide
            it.

            Indices can be obtained using [`AutoTokenizer`]. See [`PreTrainedTokenizer.encode`] and
            [`PreTrainedTokenizer.__call__`] for details.

            [What are input IDs?](../glossary#input-ids)
        attention_mask (`torch.Tensor` of shape `(batch_size, sequence_length)`, *optional*):
            Mask to avoid performing attention on padding token indices. Mask values selected in `[0, 1]`:

            - 1 for tokens that are **not masked**,
            - 0 for tokens that are **masked**.

            [What are attention masks?](../glossary#attention-mask)

            Indices can be obtained using [`AutoTokenizer`]. See [`PreTrainedTokenizer.encode`] and
            [`PreTrainedTokenizer.__call__`] for details.

            If `past_key_values` is used, optionally only the last `decoder_input_ids` have to be input (see
            `past_key_values`).

            If you want to change padding behavior, you should read [`modeling_opt._prepare_decoder_attention_mask`]
            and modify to your needs. See diagram 1 in [the paper](https://arxiv.org/abs/1910.13461) for more
            information on the default strategy.

            - 1 indicates the head is **not masked**,
            - 0 indicates the head is **masked**.
        position_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
            Indices of positions of each input sequence tokens in the position embeddings. Selected in the range `[0,
            config.n_positions - 1]`.

            [What are position IDs?](../glossary#position-ids)
        past_key_values (`tuple(tuple(torch.FloatTensor))`, *optional*, returned when `use_cache=True` is passed or when `config.use_cache=True`):
            Tuple of `tuple(torch.FloatTensor)` of length `config.n_layers`, with each tuple having 2 tensors of shape
            `(batch_size, num_heads, sequence_length, embed_size_per_head)`) and 2 additional tensors of shape
            `(batch_size, num_heads, encoder_sequence_length, embed_size_per_head)`.

            Contains pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention
            blocks) that can be used (see `past_key_values` input) to speed up sequential decoding.

            If `past_key_values` are used, the user can optionally input only the last `decoder_input_ids` (those that
            don't have their past key value states given to this model) of shape `(batch_size, 1)` instead of all
            `decoder_input_ids` of shape `(batch_size, sequence_length)`.
        inputs_embeds (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`, *optional*):
            Optionally, instead of passing `input_ids` you can choose to directly pass an embedded representation. This
            is useful if you want more control over how to convert `input_ids` indices into associated vectors than the
            model's internal embedding lookup matrix.
        use_cache (`bool`, *optional*):
            If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding (see
            `past_key_values`).
        output_attentions (`bool`, *optional*):
            Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned
            tensors for more detail.
        output_hidden_states (`bool`, *optional*):
            Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors for
            more detail.
        return_dict (`bool`, *optional*):
            Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
"""


@add_start_docstrings(
    "The bare SENTIA encoder-decoder Model outputting raw hidden-states without any specific head on top.",
    LLAMA_START_DOCSTRING,
)
class SENTIAModel(SENTIAPreTrainedModel):
    """
    Transformer decoder consisting of *config.num_hidden_layers* layers. Each layer is a [`SENTIADecoderLayer`] or [`SENTIAEncoderLayer`]

    Args:
        config: LlamaConfig
    """

    def __init__(self, config: SENTIAConfig):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.config = config
        self.vocab_size = config.vocab_size
        config.add_cross_attention = True

        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        self.posenc = PositionalEncoding(config.hidden_dim, config.hidden_dim)
        self.decoder_layers = SENTIASequential()
        self.encoder_layers = SENTIASequential()
        self.encoder_layers.add_module("embedding", self.embed_tokens)
        for i in range(config.num_hidden_layers // 2):
            decoder = SENTIADecoderLayer(config)
            encoder = SENTIAEncoderLayer(config)
            self.decoder_layers.add_module(f'SENTIADecoder{i}', decoder)
            self.encoder_layers.add_module(f'SENTIAEncoder{i}', encoder)
        self.norm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        #self.mepa = MEPA(config)

        self.gradient_checkpointing = False
        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.embed_tokens

    def set_input_embeddings(self, value):
        self.embed_tokens = value

    # Copied from transformers.models.bart.modeling_bart.BartDecoder._prepare_decoder_attention_mask
    def _prepare_decoder_attention_mask(self, attention_mask, input_shape, inputs_embeds, past_key_values_length):
        # create causal mask
        # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
        combined_attention_mask = None
        if input_shape[-1] > 1:
            combined_attention_mask = _make_causal_mask(
                input_shape,
                inputs_embeds.dtype,
                device=inputs_embeds.device,
                past_key_values_length=0,
            )

        if attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            if attention_mask.dim() == 2:
                expanded_attn_mask = _expand_mask(attention_mask, inputs_embeds.dtype, tgt_len=input_shape[-1]).to(
                    inputs_embeds.device
                )
                combined_attention_mask = (
                    expanded_attn_mask if combined_attention_mask is None else expanded_attn_mask + combined_attention_mask
                )

        return combined_attention_mask

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    def forward(
            self,
            input_ids: Optional[torch.LongTensor] = None,
            decoder_input_ids: Optional[torch.LongTensor] = None,
            decoder_inputs_embeds: Optional[torch.Tensor] = None,
            encoder_outputs: Optional[torch.Tensor] = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            labels: Optional[torch.Tensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = False,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # retrieve input_ids and inputs_embeds
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both decoder_input_ids and decoder_inputs_embeds at the same time")
        elif input_ids is not None:
            batch_size, seq_length = input_ids.shape
        elif inputs_embeds is not None:
            batch_size, seq_length, _ = inputs_embeds.shape
        else:
            seq_length = decoder_input_ids.size(1)
            padding_length = self.config.hidden_dim - seq_length
            if padding_length > 0:
                padding_tensor = torch.tensor([self.config.pad_token_id] * padding_length, dtype=torch.long, device=self.device)
                decoder_input_ids = torch.cat((padding_tensor.unsqueeze(0), decoder_input_ids), dim=-1)
            decoder_input_ids = self.embed_tokens(decoder_input_ids)
            batch_size, seq_length, _ = decoder_input_ids.shape

        seq_length_with_past = seq_length
        past_key_values_length = 0

        if past_key_values is not None:
            past_key_values_length = past_key_values[0][0].shape[2]
            seq_length_with_past = seq_length_with_past + past_key_values_length

        if position_ids is None:
            try:
                device = input_ids.device if input_ids is not None else inputs_embeds.device
            except:
                device = decoder_input_ids.device
            position_ids = torch.arange(
                0, seq_length, dtype=torch.long, device=device
            )
            position_ids = position_ids.unsqueeze(0).view(-1, seq_length)
        else:
            position_ids = position_ids.view(-1, seq_length).long()
        if (labels is not None) and (decoder_input_ids is None and decoder_inputs_embeds is None):
            decoder_input_ids = self.embed_tokens(self._shift_right(labels))
        elif (input_ids is not None) and (decoder_input_ids is None and decoder_inputs_embeds is None):
            decoder_input_ids = self.embed_tokens(self._shift_right(input_ids))
        # embed positions
        if attention_mask is None:
            attention_mask = torch.ones(
                (batch_size, seq_length_with_past), dtype=torch.bool, device=input_ids.device
            )
        attention_mask = self._prepare_decoder_attention_mask(
            attention_mask, (batch_size, seq_length), decoder_input_ids, past_key_values_length
        )

        hidden_states = input_ids

        if self.gradient_checkpointing and self.training:
            if use_cache:
                logger.warning_once(
                    "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`..."
                )
                use_cache = False
        # encoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None
        if encoder_outputs is None:
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            past_key_value = past_key_values if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                            # None for past_key_value
                        return module(*inputs, past_key_value, output_attentions)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                        create_custom_forward(self.encoder_layers),
                        hidden_states,
                        None,
                        position_ids,
                    )
            else:
                layer_outputs, attn = self.encoder_layers.forward(
                        hidden_states,
                        position_ids=position_ids,
                        past_key_value=None,
                        output_attentions=output_attentions,
                        use_cache=use_cache,
                        return_dict=False,
                    )
            encoder_outputs = layer_outputs[0]
            hidden_states = encoder_outputs
        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None
        try:
            encoder_outputs = encoder_outputs.last_hidden_state
        except:
            pass
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        past_key_value = past_key_values if past_key_values is not None else None

        if self.gradient_checkpointing and self.training:

            def create_custom_forward(module):
                def custom_forward(*inputs):
                        # None for past_key_value
                    return module(*inputs, past_key_value, output_attentions)

                return custom_forward

            layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(self.decoder_layers),
                    decoder_input_ids,
                    attention_mask,
                    position_ids,
                )
        else:
            layer_outputs, attn = self.decoder_layers.forward(
                    decoder_input_ids,
                    decoder_attention_mask=attention_mask,
                    encoder_attention_mask=None,
                    encoder_hidden_states=encoder_outputs,
                    position_ids=position_ids,
                    past_key_value=past_key_value,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                    return_dict=False
                )

        hidden_states = layer_outputs[0]

        if use_cache:
            next_decoder_cache += (layer_outputs[2 if output_attentions else 1],)

        if output_attentions:
            all_self_attns += (layer_outputs[1],)
        #hidden_states = hidden_states + self.mepa(attn)
        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if not return_dict:
            return tuple(v for v in [hidden_states, next_cache, all_hidden_states, all_self_attns] if v is not None)
        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )


@add_start_docstrings(
    "The bare SENTIA Decoder-only/Encoder-only Model outputting raw hidden-states without any specific head on top.",
    LLAMA_START_DOCSTRING,
)
class SENTIADecoderModel(SENTIAPreTrainedModel):
    """
    Transformer decoder consisting of *config.num_hidden_layers* layers. Each layer is a [`LlamaDecoderLayer`]

    Args:
        config: LlamaConfig
    """

    def __init__(self, config: SENTIAConfig):
        super().__init__(config)
        config.add_cross_attention = False
        self.config = config

        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size

        self.embed_tokens = nn.Embedding(config.vocab_size, config.n_embd, self.padding_idx)
        self.layers = nn.ModuleList([SENTIADecoderLayer(config) for _ in range(config.num_hidden_layers)])
        self.wr = nn.Linear(config.n_embd, config.hidden_dim)
        self.posenc = PositionalEncoding(config.hidden_dim, config.hidden_dim)
        self.norm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        #self.mepa = MEPA(config)

        self.gradient_checkpointing = False
        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.embed_tokens

    def set_input_embeddings(self, value):
        self.embed_tokens = value

    # Copied from transformers.models.bart.modeling_bart.BartDecoder._prepare_decoder_attention_mask
    @staticmethod
    def _prepare_decoder_attention_mask(attention_mask, input_shape, inputs_embeds, past_key_values_length):
        # create causal mask
        # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
        combined_attention_mask = None
        if input_shape[-1] > 1:
            combined_attention_mask = _make_causal_mask(
                input_shape,
                inputs_embeds.dtype,
                device=inputs_embeds.device,
                past_key_values_length=past_key_values_length,
            )

        if attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            expanded_attn_mask = _expand_mask(attention_mask, inputs_embeds.dtype, tgt_len=input_shape[-1]).to(
                inputs_embeds.device
            )
            combined_attention_mask = (
                expanded_attn_mask if combined_attention_mask is None else expanded_attn_mask + combined_attention_mask
            )

        return combined_attention_mask

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = False,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # retrieve input_ids and inputs_embeds
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both decoder_input_ids and decoder_inputs_embeds at the same time")
        elif input_ids is not None:
            batch_size, seq_length = input_ids.shape
        elif inputs_embeds is not None:
            batch_size, seq_length, _ = inputs_embeds.shape
        else:
            raise ValueError("You have to specify either decoder_input_ids or decoder_inputs_embeds")

        seq_length_with_past = seq_length
        past_key_values_length = 0

        if past_key_values is not None:
            past_key_values_length = past_key_values[0][0].shape[2]
            seq_length_with_past = seq_length_with_past + past_key_values_length

        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(
                past_key_values_length, seq_length + past_key_values_length, dtype=torch.long, device=device
            )
            position_ids = position_ids.unsqueeze(0).view(-1, seq_length)
        else:
            position_ids = position_ids.view(-1, seq_length).long()

        if inputs_embeds is None:
            inputs_embeds = self.wr(self.embed_tokens(input_ids))
        # embed positions
        if attention_mask is None:
            attention_mask = torch.ones(
                (batch_size, seq_length_with_past), dtype=torch.bool, device=inputs_embeds.device
            )
        attention_mask = self._prepare_decoder_attention_mask(
            attention_mask, (batch_size, seq_length), inputs_embeds, past_key_values_length
        )

        hidden_states = inputs_embeds
        hidden_states = self.posenc(hidden_states)

        if self.gradient_checkpointing and self.training:
            if use_cache:
                logger.warning_once(
                    "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`..."
                )
                use_cache = False

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None

        for idx, decoder_layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            past_key_value = past_key_values[idx] if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, past_key_value, output_attentions)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(decoder_layer),
                    hidden_states,
                    attention_mask,
                    position_ids,
                )
            else:
                layer_outputs, attn = decoder_layer(
                    hidden_states,
                    decoder_attention_mask=attention_mask,
                    position_ids=position_ids,
                    past_key_value=past_key_value,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                    return_dict=False,
                )

            hidden_states = layer_outputs[0]

            if use_cache:
                next_decoder_cache += (layer_outputs[2 if output_attentions else 1],)

            if output_attentions:
                all_self_attns += (layer_outputs[1],)
        #hidden_states = hidden_states + self.mepa(attn)

        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if not return_dict:
            return tuple(v for v in [hidden_states, next_cache, all_hidden_states, all_self_attns] if v is not None)
        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )


class SENTIAForCausalLM(SENTIAPreTrainedModel):
    _tied_weights_keys = ["lm_head.weight"]

    def __init__(self, config: SENTIAConfig):
        super().__init__(config)
        self.config = config
        self.model = SENTIADecoderModel(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.model.embed_tokens

    def set_input_embeddings(self, value):
        self.model.embed_tokens = value

    def get_output_embeddings(self):
        return self.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.lm_head = new_embeddings

    def set_decoder(self, decoder):
        self.model = decoder

    def get_decoder(self):
        return self.model

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=CausalLMOutputWithPast, config_class=_CONFIG_FOR_DOC)
    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            labels: Optional[torch.LongTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained(PATH_TO_CONVERTED_WEIGHTS)
        >>> tokenizer = AutoTokenizer.from_pretrained(PATH_TO_CONVERTED_TOKENIZER)

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # decoder outputs consists of (dec_features, layer_state, dec_hidden, dec_attn)
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(self.vocab_size // self.config.pretraining_tp, dim=0)
            logits = [F.linear(hidden_states, lm_head_slices[i]) for i in range(self.config.pretraining_tp)]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None
        if labels is not None:
            # Flatten the tokens
            # Enable model parallelism
            labels = labels.to(logits.device)
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            batch_size, seq_length, vocab_size = shift_logits.shape
            loss_fct = CrossEntropyLoss(ignore_index=-100)
            loss = loss_fct(
                shift_logits.view(batch_size * seq_length, vocab_size), shift_labels.view(batch_size * seq_length)
            )

        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    def prepare_inputs_for_generation(
            self, input_ids, past_key_values=None, attention_mask=None, inputs_embeds=None, **kwargs
    ):
        if past_key_values:
            input_ids = input_ids[:, -1:]

        position_ids = kwargs.get("position_ids", None)
        if attention_mask is not None and position_ids is None:
            # create position_ids on the fly for batch generation
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)
            if past_key_values:
                position_ids = position_ids[:, -1].unsqueeze(-1)

        # if `inputs_embeds` are passed, we only want to use them in the 1st generation step
        if inputs_embeds is not None and past_key_values is None:
            model_inputs = {"inputs_embeds": inputs_embeds}
        else:
            model_inputs = {"input_ids": input_ids}

        model_inputs.update(
            {
                "position_ids": position_ids,
                "past_key_values": past_key_values,
                "use_cache": kwargs.get("use_cache"),
                "attention_mask": attention_mask,
            }
        )
        return model_inputs

    @staticmethod
    def _reorder_cache(past_key_values, beam_idx):
        reordered_past = ()
        for layer_past in past_key_values:
            reordered_past += (
                tuple(past_state.index_select(0, beam_idx.to(past_state.device)) for past_state in layer_past),
            )
        return reordered_past


@add_start_docstrings(
    """
    The LLaMa Model transformer with a sequence classification head on top (linear layer).

    [`LlamaForSequenceClassification`] uses the last token in order to do the classification, as other causal models
    (e.g. GPT-2) do.

    Since it does classification on the last token, it requires to know the position of the last token. If a
    `pad_token_id` is defined in the configuration, it finds the last token that is not a padding token in each row. If
    no `pad_token_id` is defined, it simply takes the last value in each row of the batch. Since it cannot guess the
    padding tokens when `inputs_embeds` are passed instead of `input_ids`, it does the same (take the last value in
    each row of the batch).
    """,
    LLAMA_START_DOCSTRING,
)
class SENTIAForSequenceClassification(SENTIAPreTrainedModel):
    def __init__(self, config: SENTIAConfig):
        super().__init__(config)
        self.config = config
        self.num_labels = config.num_labels
        self.model = SENTIADecoderModel(config)
        self.score = nn.Linear(config.hidden_size, self.num_labels, bias=False)

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.model.embed_tokens

    def set_input_embeddings(self, value):
        self.model.embed_tokens = value

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            labels: Optional[torch.LongTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, SequenceClassifierOutputWithPast]:
        r"""
        labels (`torch.LongTensor` of shape `(batch_size,)`, *optional*):
            Labels for computing the sequence classification/regression loss. Indices should be in `[0, ...,
            config.num_labels - 1]`. If `config.num_labels == 1` a regression loss is computed (Mean-Square loss), If
            `config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        transformer_outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        hidden_states = transformer_outputs[0]
        logits = self.score(hidden_states)

        if input_ids is not None:
            batch_size = input_ids.shape[0]
        else:
            batch_size = inputs_embeds.shape[0]

        if self.config.pad_token_id is None and batch_size != 1:
            raise ValueError("Cannot handle batch sizes > 1 if no padding token is defined.")
        if self.config.pad_token_id is None:
            sequence_lengths = -1
        else:
            if input_ids is not None:
                sequence_lengths = (torch.eq(input_ids, self.config.pad_token_id).long().argmax(-1) - 1).to(
                    logits.device
                )
            else:
                sequence_lengths = -1

        pooled_logits = logits[torch.arange(batch_size, device=logits.device), sequence_lengths]

        loss = None
        if labels is not None:
            labels = labels.to(logits.device)
            if self.config.problem_type is None:
                if self.num_labels == 1:
                    self.config.problem_type = "regression"
                elif self.num_labels > 1 and (labels.dtype == torch.long or labels.dtype == torch.int):
                    self.config.problem_type = "single_label_classification"
                else:
                    self.config.problem_type = "multi_label_classification"

            if self.config.problem_type == "regression":
                loss_fct = MSELoss()
                if self.num_labels == 1:
                    loss = loss_fct(pooled_logits.squeeze(), labels.squeeze())
                else:
                    loss = loss_fct(pooled_logits, labels)
            elif self.config.problem_type == "single_label_classification":
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(pooled_logits.view(-1, self.num_labels), labels.view(-1))
            elif self.config.problem_type == "multi_label_classification":
                loss_fct = BCEWithLogitsLoss()
                loss = loss_fct(pooled_logits, labels)
        if not return_dict:
            output = (pooled_logits,) + transformer_outputs[1:]
            return ((loss,) + output) if loss is not None else output
        return SequenceClassifierOutputWithPast(
            loss=loss,
            logits=pooled_logits,
            past_key_values=transformer_outputs.past_key_values,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )


@add_start_docstrings("""
An encoder-decoder version of SENTIA designed for ConditionalGeneration and QuestionAnswering
""",
                      LLAMA_START_DOCSTRING)
class SENTIAForConditionalGeneration(SENTIAPreTrainedModel):
    _tied_weights_keys = ["lm_head.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.config.is_encoder_decoder = True
        self.model = SENTIAModel(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.model.embed_tokens

    def set_input_embeddings(self, value):
        self.model.embed_tokens = value

    def get_output_embeddings(self):
        return self.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.lm_head = new_embeddings

    def set_decoder(self, decoder):
        self.model.decoder_layers = decoder

    def get_decoder(self):
        return self.model.decoder_layers
    def set_encoder(self, encoder):
        self.model.encoder_layers = encoder
    def get_encoder(self):
        return self.model.encoder_layers
    @staticmethod
    def _prepare_decoder_attention_mask(attention_mask, input_shape, inputs_embeds, past_key_values_length):
        # create causal mask
        # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
        combined_attention_mask = None
        if input_shape[-1] > 1:
            combined_attention_mask = _make_causal_mask(
                input_shape,
                inputs_embeds.dtype,
                device=inputs_embeds.device,
                past_key_values_length=past_key_values_length,
            )

        if attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            expanded_attn_mask = _expand_mask(attention_mask, inputs_embeds.dtype, tgt_len=input_shape[-1]).to(
                inputs_embeds.device
            )
            combined_attention_mask = (
                expanded_attn_mask if combined_attention_mask is None else expanded_attn_mask + combined_attention_mask
            )

        return combined_attention_mask
    

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=Seq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
    def forward(
            self,
            input_ids: Optional[torch.LongTensor] = None,
            encoder_outputs: Optional[torch.Tensor] = None,
            decoder_input_ids: Optional[torch.LongTensor] = None,
            decoder_input_embeds: Optional[torch.Tensor] = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            labels: Optional[torch.LongTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, Seq2SeqLMOutput]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained(PATH_TO_CONVERTED_WEIGHTS)
        >>> tokenizer = AutoTokenizer.from_pretrained(PATH_TO_CONVERTED_TOKENIZER)

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        outputs = self.model.forward(
            input_ids=input_ids,
            decoder_input_ids=decoder_input_ids,
            decoder_inputs_embeds=decoder_input_embeds,
            attention_mask=attention_mask,
            encoder_outputs=encoder_outputs,
            position_ids=position_ids,
            past_key_values=past_key_values,
            labels=labels,
            inputs_embeds=None,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(self.vocab_size // self.config.pretraining_tp, dim=0)
            logits = [F.linear(hidden_states, lm_head_slices[i]) for i in range(self.config.pretraining_tp)]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None
        if labels is not None:
            # Shift so that tokens < n predict n
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = CrossEntropyLoss(ignore_index=-100)
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)

        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output

        return Seq2SeqLMOutput(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            decoder_hidden_states=outputs.hidden_states,
            decoder_attentions=outputs.attentions,
        )

    @staticmethod
    def _reorder_cache(past_key_values, beam_idx):
        reordered_past = ()
        for layer_past in past_key_values:
            reordered_past += (
                tuple(past_state.index_select(0, beam_idx.to(past_state.device)) for past_state in layer_past),
            )
        return reordered_past

    def prepare_inputs_for_generation(
            self,
            input_ids,
            past_key_values=None,
            attention_mask=None,
            use_cache=None,
            encoder_outputs=None,
            **kwargs,
    ):
        return {
            "decoder_input_ids": input_ids,
            "past_key_values": past_key_values,
            "encoder_outputs": encoder_outputs,
            "attention_mask": attention_mask,
            "use_cache": use_cache,
            **kwargs,
        }
    def _prepare_attention_mask_for_generation(self, inputs: torch.Tensor, pad_token_id: int = None, eos_token_id: Union[int,  List[int]] = None) -> torch.LongTensor:
        attn = super()._prepare_attention_mask_for_generation(inputs, pad_token_id, eos_token_id)
        if attn.dim() == 2:
            attn = _expand_mask(attn, torch.float16,).to(dtype=torch.long)
        return attn
    

    def prepare_decoder_input_ids_from_labels(self, labels: torch.Tensor):
        return self._shift_right(labels)


@add_start_docstrings(
    "The bare SENTIA encoder-decoder Model outputting raw hidden-states without any specific head on top.",
    LLAMA_START_DOCSTRING,
)
class SENTIAForImageGeneration(SENTIAPreTrainedModel):
    """
    Transformer decoder consisting of *config.num_hidden_layers* layers. Each layer is a [`LlamaDecoderLayer`]

    Args:
        config: LlamaConfig
    """

    def __init__(self, config: SENTIAConfig):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.config = config
        self.vocab_size = config.vocab_size
        config.add_cross_attention = True

        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size, self.padding_idx)
        self.decoder_layers = nn.ModuleList([SENTIADecoderLayer(config) for _ in range(config.num_hidden_layers // 2)])
        self.latent = nn.Sequential(
            nn.Conv1d(config.hidden_dim, config.n_inner, kernel_size=3, padding=1),
            nn.ReLU(True),
            nn.Conv1d(config.n_inner, config.hidden_dim, kernel_size=3, padding=1),
            nn.ReLU(True),
            nn.MaxPool1d(kernel_size=2, stride=2)

        )
        self.encoder_layers = nn.ModuleList([SENTIAEncoderLayer(config) for _ in range(config.num_hidden_layers // 2)])
        self.norm = SENTIARMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.mepa = MEPA(config)
        self.generator = nn.Sequential(
            nn.Linear(config.hidden_dim, config.n_inner),
            nn.GELU(),
            nn.Linear(config.n_inner, 1024 * 1024 * 3),

        )

        self.gradient_checkpointing = False
        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.embed_tokens

    def set_input_embeddings(self, value):
        self.embed_tokens = value

    # Copied from transformers.models.bart.modeling_bart.BartDecoder._prepare_decoder_attention_mask
    def _prepare_decoder_attention_mask(self, attention_mask, input_shape, inputs_embeds, past_key_values_length):
        # create causal mask
        # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
        combined_attention_mask = None
        if input_shape[-1] > 1:
            combined_attention_mask = torch.ones(input_shape, dtype=inputs_embeds.dtype,)

        if attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            expanded_attn_mask = _expand_mask(attention_mask, inputs_embeds.dtype, tgt_len=input_shape[-1]).to(
                inputs_embeds.device
            )
            combined_attention_mask = (
                expanded_attn_mask if combined_attention_mask is None else expanded_attn_mask + combined_attention_mask
            )

        return combined_attention_mask

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    def forward(
            self,
            input_ids: torch.LongTensor = None,
            decoder_input_ids: Optional[torch.LongTensor] = None,
            decoder_inputs_embeds: Optional[torch.Tensor] = None,
            attention_mask: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.LongTensor] = None,
            labels: Optional[torch.Tensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = False,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # retrieve input_ids and inputs_embeds
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both decoder_input_ids and decoder_inputs_embeds at the same time")
        elif input_ids is not None:
            batch_size, seq_length = input_ids.shape
        elif inputs_embeds is not None:
            batch_size, seq_length, _ = inputs_embeds.shape
        else:
            raise ValueError("You have to specify either decoder_input_ids or decoder_inputs_embeds")

        seq_length_with_past = seq_length
        past_key_values_length = 0

        if past_key_values is not None:
            past_key_values_length = past_key_values[0][0].shape[2]
            seq_length_with_past = seq_length_with_past + past_key_values_length

        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(
                past_key_values_length, seq_length + past_key_values_length, dtype=torch.long, device=device
            )
            position_ids = position_ids.unsqueeze(0).view(-1, seq_length)
        else:
            position_ids = position_ids.view(-1, seq_length).long()

        if (labels is not None) and (decoder_input_ids is None and decoder_inputs_embeds is None):
            decoder_input_ids = self._shift_right(labels)
        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)
        decoder_input_ids = self.embed_tokens(decoder_input_ids)
        # embed positions
        if attention_mask is None:
            attention_mask = torch.ones(
                (batch_size, seq_length_with_past), dtype=torch.bool, device=inputs_embeds.device
            )
        attention_mask = self._prepare_decoder_attention_mask(
            attention_mask, (batch_size, seq_length), inputs_embeds, past_key_values_length
        )

        hidden_states = inputs_embeds

        if self.gradient_checkpointing and self.training:
            if use_cache:
                logger.warning_once(
                    "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`..."
                )
                use_cache = False
        # encoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None
        decoder_states = hidden_states
        for idx, encoder_layer in enumerate(self.encoder_layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            past_key_value = past_key_values[idx] if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, past_key_value, output_attentions)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(encoder_layer),
                    hidden_states,
                    attention_mask,
                    position_ids,
                )
            else:
                layer_outputs = encoder_layer(
                    hidden_states,
                    attention_mask=attention_mask,
                    position_ids=position_ids,
                    past_key_value=past_key_value,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                )
        hidden_states = layer_outputs[0]
        residual = hidden_states
        hidden_states = self.latent(hidden_states)
        hidden_states = hidden_states + residual
        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None
        encoder_mask = self._prepare_decoder_attention_mask(
            torch.ones((batch_size, seq_length_with_past), dtype=torch.bool, device=inputs_embeds.device)
            , (batch_size, seq_length)
            , inputs_embeds
            , past_key_values_length)

        for idx, decoder_layer in enumerate(self.decoder_layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            past_key_value = past_key_values[idx] if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, past_key_value, output_attentions)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(decoder_layer),
                    decoder_input_ids,
                    attention_mask,
                    position_ids,
                )
            else:
                layer_outputs = decoder_layer.forward(
                    decoder_input_ids,
                    attention_mask=attention_mask,
                    encoder_attention_mask=encoder_mask,
                    encoder_hidden_states=hidden_states,
                    position_ids=position_ids,
                    past_key_value=past_key_value,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                )

            hidden_states = layer_outputs[0]

            if use_cache:
                next_decoder_cache += (layer_outputs[2 if output_attentions else 1],)

            if output_attentions:
                all_self_attns += (layer_outputs[1],)
        hidden_states = hidden_states + self.mepa(layer_outputs[0])

        hidden_states = self.norm(hidden_states)
        hidden_states = self.generator(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if not return_dict:
            return tuple(v for v in [hidden_states, next_cache, all_hidden_states, all_self_attns] if v is not None)
        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )
