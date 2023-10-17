
from transformers import GPT2Tokenizer, GPT2TokenizerFast

# Just using GPT-2's tokenizer
class SENTIATokenizer(GPT2Tokenizer):
    def __init__(self,
        vocab_file,
        merges_file,
        errors="replace",
        unk_token="<|endoftext|>",
        bos_token="<s>",
        eos_token="<|endoftext|>",
        pad_token=None,
        add_prefix_space=False,
        add_bos_token=False,
        **kwargs,):
        super(SENTIATokenizer, self).__init__(self,
        vocab_file,
        merges_file,
        errors,
        unk_token,
        bos_token,
        eos_token,
        pad_token,
        add_prefix_space,
        add_bos_token,
        **kwargs,)
class SENTIATokenizerFast(GPT2TokenizerFast):
    def __init__(self,
        vocab_file=None,
        merges_file=None,
        tokenizer_file=None,
        unk_token="<|endoftext|>",
        bos_token="<s>",
        eos_token="<|endoftext|>",
        add_prefix_space=False,
        **kwargs,):
        super(SENTIATokenizerFast, self).__init__(vocab_file,
        merges_file,
        tokenizer_file,
        unk_token,
        bos_token,
        eos_token,
        add_prefix_space,
        **kwargs,)