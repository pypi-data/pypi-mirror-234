import torch


class Attention_Agg(torch.nn.Module):
    """Aggregate vertors of the last layer of encoders.

    Args:
        input_size (int): input vector size.
        hidden_size (int): hidden size.
        dropout_rate (float, optional): dropout rate. Defaults to 0.1.
    """

    def __init__(self, input_size: int, hidden_size: int, dropout_rate: float = 0.1):
        super().__init__()
        self.dropout_rate = dropout_rate

        self.ff1 = torch.nn.Linear(input_size, hidden_size)
        self.ff2 = torch.nn.Linear(hidden_size, 1, bias=False)
        if dropout_rate is not None:
            self.model_drop = torch.nn.Dropout(dropout_rate)

    def forward(
        self, input_tensor: torch.FloatTensor, mask: torch.FloatTensor = None
    ) -> torch.FloatTensor:
        """work flow.

        Args:
            input_tensor (torch.FloatTensor): input tensor.
            mask (torch.FloatTensor, optional): attention mask. Defaults to None.

        Returns:
            torch.FloatTensor: output tensor.
        """
        attn = torch.tanh(self.ff1(input_tensor))
        attn = self.ff2(attn).squeeze(2)
        if mask is not None:
            attn = attn.masked_fill(mask == 0, -1e9)
        attn = torch.softmax(attn, dim=1)
        # dropout method 2.
        if self.dropout_rate is not None:
            attn = self.model_drop(attn)
        ctx_vec = torch.bmm(attn.unsqueeze(1), input_tensor).squeeze(1)
        return ctx_vec
