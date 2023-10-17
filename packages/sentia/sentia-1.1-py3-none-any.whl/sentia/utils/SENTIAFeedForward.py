import torch.nn as nn

class SENTIAFF(nn.Module):
    def __init__(self, d_model, d_inner=2048, *args, **kwargs):
        super(SENTIAFF, self).__init__(*args, **kwargs)
        self.linear1 = nn.Linear(d_model, d_inner)
        self.act = nn.ReLU()
        self.linear2 = nn.Linear(d_inner, d_model)

    def forward(self, x):
        x = self.linear1(x)
        x = self.act(x)
        y = self.linear2(x)
        return y