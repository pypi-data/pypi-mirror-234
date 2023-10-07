from typing import Any, List

import torch
from torch.autograd import Variable
from transformers import AutoTokenizer, XLMRobertaModel

from exciton.ml.classification.utils import Attention_Agg


class Classfication_Model(object):
    """Classification Model.

    Args:
        drop_rate (float, optional): dropout rate. Defaults to 0.1.
        n_labels (int, optional): number of labels. Defaults to 0.
        device (str, optional): device. Defaults to "cpu".
    """

    def __init__(self, drop_rate: float = 0.1, n_labels: int = 0, device: str = "cpu"):
        self.drop_rate = drop_rate
        self.n_labels = n_labels
        self.device = torch.device(device)
        self.train_modules = {}
        self.base_modules = {}
        self.batch_data = {}
        self.tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

    def build_modules(self):
        """Declare all modules in your model."""
        hidden_size = 768
        self.base_modules["embedding"] = XLMRobertaModel.from_pretrained(
            "xlm-roberta-base", output_hidden_states=True, output_attentions=True
        ).to(self.device)
        self.TOK_START = 0
        self.TOK_END = 2
        self.TOK_PAD = 1
        self.train_modules["attn_agg"] = Attention_Agg(
            hidden_size, hidden_size, self.drop_rate
        ).to(self.device)
        self.train_modules["ff"] = torch.nn.Linear(hidden_size, hidden_size).to(
            self.device
        )
        self.train_modules["classifier"] = torch.nn.Linear(
            hidden_size, self.n_labels
        ).to(self.device)
        self.train_modules["drop"] = torch.nn.Dropout(self.drop_rate).to(self.device)

    def _init_model_parameters(self):
        """load model param"""
        for model_name in self.base_modules:
            self.base_modules[model_name].eval()
            model_file = "{}/{}.model".format(self.path_to_model, model_name)
            self.base_modules[model_name].load_state_dict(
                torch.load(model_file, map_location=lambda storage, loc: storage)
            )
        for model_name in self.train_modules:
            self.train_modules[model_name].eval()
            model_file = "{}/{}.model".format(self.path_to_model, model_name)
            self.train_modules[model_name].load_state_dict(
                torch.load(model_file, map_location=lambda storage, loc: storage)
            )

    def _build_pipe(self):
        """Shared pipe"""
        with torch.no_grad():
            input_emb = self.base_modules["embedding"](
                self.batch_data["input_ids"],
                self.batch_data["pad_mask"],
            )
            input_emb = input_emb[0]
        doc_vec = self.train_modules["attn_agg"](
            input_emb, self.batch_data["attn_mask"]
        )
        fc = torch.relu(self.train_modules["drop"](self.train_modules["ff"](doc_vec)))
        logits = self.train_modules["drop"](self.train_modules["classifier"](fc))
        return logits

    def _build_batch(self, batch_raw: List[Any]):
        """Build Batch

        Args:
            batch_data (List[Any]): batch data.
        """
        tokens_arr = []
        input_data_raw = []
        max_length = 0
        for itm in batch_raw:
            out = self.tokenizer.encode(itm["text"])[1:-1]
            tokens_arr.append(out["tokens"])
            if max_length < len(out["tokens"]):
                max_length = len(out["tokens"])
            input_data_raw.append(itm)
        tokens_out = []
        for itm in tokens_arr:
            itm = itm[:max_length]
            itm += [self.TOK_PAD for _ in range(max_length - len(itm))]
            itm = [self.TOK_START] + itm + [self.TOK_END]
            tokens_out.append(itm)
        tokens_var = Variable(torch.LongTensor(tokens_out))
        # padding mask.
        pad_mask = Variable(torch.FloatTensor(tokens_out))
        pad_mask[pad_mask != float(self.TOK_PAD)] = -1.0
        pad_mask[pad_mask == float(self.TOK_PAD)] = 0.0
        pad_mask = -pad_mask
        # attention mask.
        attn_mask = Variable(torch.FloatTensor(tokens_out))
        attn_mask[attn_mask == float(self.TOK_START)] = -1.0
        attn_mask[attn_mask == float(self.TOK_END)] = -1.0
        attn_mask[attn_mask == float(self.TOK_PAD)] = -1.0
        attn_mask[attn_mask != -1.0] = 0.0
        attn_mask = attn_mask + 1.0
        # batch_data
        self.batch_data["max_length"] = max_length
        self.batch_data["input_ids"] = tokens_var.to(self.device)
        self.batch_data["pad_mask"] = pad_mask.to(self.device)
        self.batch_data["attn_mask"] = attn_mask.to(self.device)
        self.batch_data["input_data_raw"] = input_data_raw
