import torch
import torch.nn as nn


class TinyClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(16, 4)

    def forward(self, x):
        return self.net(x)


def main():
    model = TinyClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    x = torch.randn(8, 16)
    y = torch.randint(0, 4, (8,))
    loss = nn.CrossEntropyLoss()(model(x), y)
    loss.backward()
    optimizer.step()
    print({"loss": float(loss)})


if __name__ == "__main__":
    main()
