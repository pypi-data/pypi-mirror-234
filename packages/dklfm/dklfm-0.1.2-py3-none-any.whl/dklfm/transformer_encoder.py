import math
import pytorch_lightning as pl
import torch
import torch.nn as nn
from torch import Tensor
from torch.nn import functional as F
from torch import nn


class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe, persistent=False)

    def forward(self, x: Tensor) -> Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


class NewGELU(nn.Module):
    """
    Implementation of the GELU activation function currently in Google BERT repo (identical to OpenAI GPT).
    Reference: Gaussian Error Linear Units (GELU) paper: https://arxiv.org/abs/1606.08415
    """
    def forward(self, x):
        return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))


class Block(nn.Module):
    """ an unassuming Transformer block """

    def __init__(self, n_embd, n_head, resid_pdrop, split_dim=2, sparse=True):
        super().__init__()
        self.split_dim = split_dim
        self.n_embd = n_embd
        resid_pdrop = resid_pdrop
        self.sparse = sparse
        if sparse:
            from fairseq.modules.sparse_multihead_attention import SparseMultiheadAttention
            self.attn = SparseMultiheadAttention(self.n_embd, n_head, dropout=0.1, self_attention=True, stride=128, expressivity=32, is_bidirectional=False)
        else:
            self.attn = nn.MultiheadAttention(self.n_embd, n_head, dropout=0.1,)

        self.ln_1 = nn.LayerNorm(self.n_embd)
        self.ln_2 = nn.LayerNorm(self.n_embd)
        self.mlp = nn.ModuleDict(dict(
            c_fc    = nn.Linear(self.n_embd, 4 * self.n_embd),
            c_proj  = nn.Linear(4 * self.n_embd, self.n_embd),
            act     = NewGELU(),
            dropout = nn.Dropout(resid_pdrop),
        ))
        m = self.mlp
        self.mlpf = lambda x: m.dropout(m.c_proj(m.act(m.c_fc(x)))) # MLP forward

    def forward(self, x, key_padding_mask=None):
        r"""
        Args:
            key_padding_mask: If specified, a mask of shape :math:`(N, S)` indicating which elements within ``key``
                to ignore for the purpose of attention (i.e. treat as "padding"). For unbatched `query`, shape should be :math:`(S)`.
                Binary and float masks are supported.
                For a binary mask, a ``True`` value indicates that the corresponding ``key`` value will be ignored for
                the purpose of attention. For a float mask, it will be directly added to the corresponding ``key`` value.
        """
        x = self.ln_1(x)
        # q shape (N, L, E_q) where N is batch, L target length
        x = x.permute(1, 0, 2)
        attn_output, _ = self.attn(x, x, x, key_padding_mask=key_padding_mask)
        attn_output = attn_output.permute(1, 0, 2)
        x = x.permute(1, 0, 2)
        x = x + attn_output
        x = x + self.mlpf(self.ln_2(x))
        return x


class TransformerEncoder(nn.Module):
    def __init__(self, input_dim, attention_dim=8, output_dim=8, num_hidden_layers=3, dropout=0.1, sparse=False):
        super().__init__()
        self.fc0 = nn.Linear(input_dim, attention_dim)
        attention_layers = []
        for _ in range(num_hidden_layers):
            attention_layers.append(Block(attention_dim, 8, dropout, sparse=sparse))
        self.attention_layers = nn.ModuleList(attention_layers)
        self.fc1 = nn.Linear(attention_dim, output_dim)
        self.positional_encoder = PositionalEncoding(attention_dim)

    def forward(self, x):
        x = self.fc0(x)
        x = F.relu(x)
        x = self.positional_encoder(x)
        for layer in self.attention_layers:
            x = layer(x)
        return self.fc1(x)