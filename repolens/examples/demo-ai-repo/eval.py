import torch

from train import TinyClassifier


def main():
    model = TinyClassifier()
    x = torch.randn(8, 16)
    logits = model(x)
    print({"logits_shape": list(logits.shape)})


if __name__ == "__main__":
    main()
