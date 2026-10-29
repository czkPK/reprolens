import tempfile
import unittest
from pathlib import Path

from repolens.scanner import scan_repo


class ScannerTests(unittest.TestCase):
    def test_demo_repo_flags(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-ai-repo"
        snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("readme"))
        self.assertTrue(snapshot.has("deps"))
        self.assertTrue(snapshot.has("train_script"))
        self.assertTrue(snapshot.has("eval_script"))
        self.assertTrue(snapshot.has("install_instructions"))
        self.assertTrue(snapshot.has("run_instructions"))
        self.assertTrue(snapshot.has("data_mention"))
        self.assertTrue(snapshot.has("expected_results"))
        self.assertFalse(snapshot.has("seed"))
        self.assertTrue(snapshot.has("ml_project"))
        self.assertFalse(snapshot.has("llm_project"))

    def test_demo_llm_repo_flags(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("llm_project"))
        self.assertTrue(snapshot.has("rag_project"))
        self.assertTrue(snapshot.has("agent_project"))
        self.assertTrue(snapshot.has("model_provider"))
        self.assertTrue(snapshot.has("model_version"))
        self.assertTrue(snapshot.has("prompt_files"))
        self.assertTrue(snapshot.has("sampling_params"))
        self.assertTrue(snapshot.has("rag_index"))
        self.assertFalse(snapshot.has("prompt_version"))
        self.assertFalse(snapshot.has("agent_trace"))
        self.assertFalse(snapshot.has("eval_dataset"))

    def test_dataset_link_is_preferred_over_paper_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[![arXiv](https://img.shields.io/badge/arXiv-2509.24979-red)](https://arxiv.org/pdf/2509.24979)\n"
                "## Data\n"
                "Download the training dataset from "
                "[Hugging Face](https://huggingface.co/datasets/example/project-data).\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
            source_ids = snapshot.evidence_for("data_source_link")
        self.assertTrue(snapshot.has("data_source_link"))
        self.assertTrue(snapshot.has("data_mention"))
        source_evidence = next(item for item in snapshot.evidence if item.id == source_ids[0])
        self.assertIn("huggingface.co/datasets", source_evidence.excerpt)
        self.assertNotIn("arxiv", source_evidence.excerpt.lower())

    def test_non_llm_model_does_not_enable_llm_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Vision model\n\n"
                "[Dataset](https://huggingface.co/datasets/example/vision-data)\n\n"
                "See the [OpenAI blog](https://openai.com/blog/example) for background.\n"
                "We train agents in simulated environments.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("llm_project"))
        self.assertFalse(snapshot.has("agent_project"))
        self.assertFalse(snapshot.has("model_provider"))
        self.assertFalse(snapshot.has("model_agnostic"))

    def test_explicit_llm_api_project_is_still_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# LLM assistant\n\n"
                "Use the OpenAI API with gpt-4o. The system message and prompt template are versioned.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("llm_project"))
        self.assertTrue(snapshot.has("model_provider"))
        self.assertTrue(snapshot.has("model_version"))

    def test_model_license_is_not_data_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Model release\n\n"
                "Download the pretrained model from https://storage.googleapis.com/example_models/model.zip .\n"
                "The code and model weights are released under the MIT License.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("model_source_link"))
        self.assertFalse(snapshot.has("data_license"))

    def test_data_license_under_data_heading_is_recognized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Dataset\n\n"
                "https://huggingface.co/datasets/example/data\n\n"
                "### Source data and license\n"
                "ExampleData is released under CC BY-NC 4.0.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("data_license"))

    def test_vision_retrieval_is_not_rag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Vision model\n\n"
                "The benchmark evaluates image-to-text retrieval and text-to-image retrieval.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("rag_project"))
        self.assertFalse(snapshot.has("llm_project"))

    def test_huggingface_docs_link_is_not_model_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Model project\n\n"
                "See the model documentation at https://huggingface.co/docs/transformers/model_doc/example.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("model_source_link"))

    def test_storage_agreement_is_not_model_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Dataset terms\n\n"
                "Trained models are distributed under the dataset terms: "
                "https://storage.googleapis.com/example/Agreement.pdf\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("model_source_link"))

    def test_generic_profiler_trace_is_not_agent_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "train.py").write_text(
                "with profiler.StepTraceAnnotation('train', step_num=1):\n    pass\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("agent_trace"))

    def test_module_style_training_command_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Training\n\n"
                "python -m example.main --config=configs/train.py --workdir=/tmp/train\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("train_instruction"))
        self.assertTrue(snapshot.has("run_instructions"))

    def test_make_sure_is_not_a_run_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Setup\n\nMake sure you have Python>=3.10 installed on your machine.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("run_instructions"))

    def test_dataset_phrase_with_downloaded_model_is_not_data_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Fine-tuning\n\n"
                "You can run fine-tuning of the downloaded model on your dataset of interest.\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("data_mention"))
        self.assertFalse(snapshot.has("data_source_link"))

    def test_cloud_drive_model_weights_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Project\n\n## Pretrained Models\n\n"
                "- **ViT-B**: [Baidu Pan](https://pan.baidu.com/s/example) (Code: abcd)\n"
                "- **CLIP**: [Google Drive](https://drive.google.com/file/d/example/view)\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("model_source_link"))
        self.assertTrue(snapshot.has("model_version"))

    def test_google_drive_model_weight_is_not_data_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backbone.py").write_text(
                "model_urls = {\n"
                "    'osnet_x1_0':\n"
                "        'https://drive.google.com/uc?id=example-model',\n"
                "}\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("model_source_link"))
        self.assertFalse(snapshot.has("data_source_link"))

    def test_code_reference_url_is_not_data_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data_dir = root / "data"
            data_dir.mkdir()
            (data_dir / "data_utils.py").write_text(
                "# based on http://stackoverflow.com/questions/7323664/example\n"
                "def preprocess_data(value):\n"
                "    return value\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertFalse(snapshot.has("data_source_link"))

    def test_google_drive_dataset_link_is_still_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Dataset\n\n"
                "Download the dataset from "
                "[Google Drive](https://drive.google.com/file/d/example-dataset/view).\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("data_source_link"))

    def test_root_install_markdown_is_searched_for_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Project\n\nSee INSTALL.md for setup.\n",
                encoding="utf-8",
            )
            (root / "INSTALL.md").write_text(
                "# Installation\n\n```bash\n"
                "conda create -n example python=3.10\n"
                "conda activate example\n"
                "pip install -r requirements.txt\n```\n",
                encoding="utf-8",
            )
            snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("install_instructions"))
        self.assertTrue(snapshot.has("run_instructions"))
        evidence_paths = {
            item.path for item in snapshot.evidence
            if item.id in snapshot.evidence_for("install_instructions", "run_instructions")
        }
        self.assertIn("INSTALL.md", evidence_paths)

    def test_claim_extraction_skips_copyright_and_docs_boilerplate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Copyright 2024 Example Team. All rights reserved.\n"
                "Full documentation can be found here: https://example.com/model\n"
                "```bash\n"
                "pip install example-package\n"
                "```\n"
                "The project supports benchmark reproduction with a fixed seed and evaluation dataset.\n",
                encoding="utf-8",
            )
            claims = [item.excerpt for item in scan_repo(root).evidence if item.kind == "claim"]
        self.assertEqual(len(claims), 1)
        self.assertIn("benchmark reproduction", claims[0])


if __name__ == "__main__":
    unittest.main()
