import unittest

from repolens.script_semantic import analyze_script


class ScriptSemanticTests(unittest.TestCase):
    def test_generic_python_script_detects_training_and_seed(self):
        text = """import torch
import torch.nn.functional as F

torch.manual_seed(42)
optimizer = torch.optim.Adam(model.parameters())
trainer.fit(model, train_loader)
"""
        signals = {signal.criterion_id: signal for signal in analyze_script("tools/pipeline.py", text)}
        self.assertIn("EXP-01", signals)
        self.assertIn("EXP-03", signals)
        self.assertEqual(signals["EXP-03"].kind, "seed-setting")

    def test_data_script_detects_dataset_loading(self):
        text = """from datasets import load_dataset
from torch.utils.data import DataLoader
ds = load_dataset("example/data")
loader = DataLoader(ds, batch_size=32)
"""
        signals = {signal.criterion_id: signal for signal in analyze_script("scripts/prepare.py", text)}
        self.assertIn("DATA-02", signals)
        self.assertEqual(signals["DATA-02"].kind, "data-script")

    def test_inference_preprocess_is_not_data_preprocessing(self):
        text = """def preprocess(image):
    return image / 255.0
"""
        self.assertEqual(analyze_script("tools/deploy/inference.py", text), [])

    def test_library_module_is_not_treated_as_entrypoint(self):
        text = """from torch.utils.data import DataLoader
loader = DataLoader(dataset, batch_size=32)
"""
        self.assertEqual(analyze_script("package/data_utils.py", text), [])

    def test_shell_training_command_is_detected(self):
        text = """#!/bin/bash
accelerate launch train.py --config configs/train.yaml
"""
        signals = {signal.criterion_id: signal for signal in analyze_script("scripts/run.sh", text)}
        self.assertIn("EXP-01", signals)
        self.assertEqual(signals["EXP-01"].kind, "training-script")


if __name__ == "__main__":
    unittest.main()
