import torch
from transformers import AutoTokenizer, BertModel

from exciton.ml.tagging.tagging_model import Tagging_Model
from exciton.ml.tagging.utils import EncoderRNN


class Tagging_Model_BERT(Tagging_Model):
    """Tagging Model.

    Args:
        drop_rate (float, optional): dropout rate. Defaults to 0.1.
        n_labels (int, optional): number of labels. Defaults to 0.
        device (str, optional): device. Defaults to "cpu".
    """

    def __init__(self, drop_rate: float = 0.1, n_labels: int = 0, device: str = "cpu"):
        super().__init__(drop_rate=drop_rate, n_labels=n_labels, device=device)
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    def build_modules(self):
        """Declare all modules in your model."""
        hidden_size = 768
        self.base_modules["embedding"] = BertModel.from_pretrained(
            "bert-base-cased", output_hidden_states=True, output_attentions=True
        ).to(self.device)
        self.TOK_START = 101
        self.TOK_END = 102
        self.TOK_PAD = 0
        self.train_modules["encoder"] = EncoderRNN(
            embedding_size=hidden_size,
            hidden_size=hidden_size,
            n_layers=2,
            rnn_network="lstm",
            device=self.device,
        ).to(self.device)
        self.train_modules["classifier"] = torch.nn.Linear(
            hidden_size * 2, self.n_labels
        ).to(self.device)
        self.train_modules["drop"] = torch.nn.Dropout(self.drop_rate).to(self.device)
