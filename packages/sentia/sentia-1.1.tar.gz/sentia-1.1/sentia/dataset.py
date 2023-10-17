from torch.utils.data import Dataset
import torch

# You may have to adjust the code a bit so that these classes fit the columns you would like to use.

class Seq2SeqDataset(Dataset):
    def __init__(self, tokenizer, data, max_length=32):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx): 
        input = self.data[idx]["translation"]["en"].strip("\n")
        input_text = f"{input}"
        target_text = self.data[idx]["translation"]["fr"].strip("\n")
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        target_ids = self.tokenizer.encode(target_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        input_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        target_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(target_ids))
        attention_mask = [True] * len(input_ids)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.int64),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.bool),
            "labels": torch.tensor(target_ids, dtype=torch.int64),
            "target_text": target_text
        }

class SENTIADataset(Dataset):
    def __init__(self, tokenizer, data, max_length=256):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if len(self.data[idx]["text"]) > self.max_length:
            self.data[idx]["text"] = self.data[idx]["text"][:self.max_length]
        text = self.data[idx]["text"].strip("\n")
        index = self.max_length // 2
        input_text = f"{text} <|endoftext|>"
        target_text = f"{text} <|endoftext|>"
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        target_ids = self.tokenizer.encode(target_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        input_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        target_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(target_ids))
        attention_mask = [True] * len(input_ids)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.int64),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.int64),
            "labels": torch.tensor(target_ids, dtype=torch.int64),
            "target_text": target_text
        }
class ConversationDataset(Dataset):
    def __init__(self, tokenizer, max_length=256, data=None):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        try:
            user = self.data[idx]["Input"] or ""
            assistant = self.data[idx]["Output"].strip('\n')
        except KeyError:
            user = self.data[idx]["question"].strip("\n")
            ans_index = self.data[idx]["answer"]
            assistant = self.data[idx]["choices"][ans_index].strip('\n')
        
        input_text = f"<|USER|> {user} <|ASSISTANT|> {assistant} <|endoftext|>"
        target_text = f"<|USER|> {user} <|ASSISTANT|> {assistant} <|endoftext|>"
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        target_ids = self.tokenizer.encode(target_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        input_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        target_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(target_ids))
        attention_mask = [1] * len(input_ids)

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.int64),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.int64).view(1, -1),
            "labels": torch.tensor(target_ids, dtype=torch.int64),
            "target_text": target_text
        }