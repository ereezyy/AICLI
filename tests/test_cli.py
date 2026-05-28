"""
Tests for ai_toolkit.py CLI.

This module tests the CLI commands defined in ai_toolkit.py, covering:
- Removal of the `awaken` command (PR change)
- Removal of top-level groq/subprocess imports (PR change)
- Correct behaviour of all remaining commands
- Error-handling paths (exception → sys.exit(1))
- Default option values
- Branching logic (deploy local vs cloud, train model types, template handling)
"""

import importlib
import importlib.util
import sys
import ast
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

# ---------------------------------------------------------------------------
# Helpers to load the CLI module with a fully-mocked ai_toolkit package.
# The ai_toolkit package cannot be imported normally after this PR because its
# submodules (data, models, training, …) were deleted.
# ---------------------------------------------------------------------------

CLI_PATH = str(Path(__file__).parent.parent / "ai_toolkit.py")


def _build_mock_ai(version="1.0.0"):
    """Return a MagicMock that satisfies the surface area used by the CLI."""
    mock_ai = MagicMock()
    mock_ai.__version__ = version

    # Config class
    mock_config = MagicMock()
    mock_config.MODEL_STORAGE_PATH = "./models"
    mock_config.DATA_STORAGE_PATH = "./data"
    mock_config.LOG_PATH = "./logs"
    mock_ai.Config = mock_config

    # get_device_info returns something printable for the info command
    mock_ai.get_device_info.return_value = {"cpu_count": 1, "gpu_count": 0}

    return mock_ai


def _load_cli(mock_ai=None):
    """
    Load ai_toolkit.py as a fresh module each time, using a pre-installed
    mock for the 'ai_toolkit' package so the module-level import succeeds.
    """
    if mock_ai is None:
        mock_ai = _build_mock_ai()

    # Remove any previously-cached CLI module.
    sys.modules.pop("ai_toolkit_cli", None)

    mock_names = [
        "ai_toolkit",
        "ai_toolkit.data",
        "ai_toolkit.models",
        "ai_toolkit.training",
        "ai_toolkit.evaluation",
        "ai_toolkit.deployment",
        "ai_toolkit.automl",
        "ai_toolkit.utils",
        "ai_toolkit.utils.project",
    ]
    saved = {name: sys.modules.get(name) for name in mock_names}
    for name in mock_names:
        sys.modules[name] = mock_ai if name == "ai_toolkit" else MagicMock()

    try:
        spec = importlib.util.spec_from_file_location("ai_toolkit_cli", CLI_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original

    return module, mock_ai


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def runner():
    # mix_stderr=True so that click.secho(..., err=True) messages are included
    # in result.output, which simplifies assertions on error messages.
    return CliRunner()


@pytest.fixture()
def cli_module():
    module, _ = _load_cli()
    return module


@pytest.fixture()
def cli_and_ai():
    """Return (cli_module, mock_ai) together so tests can inspect calls."""
    return _load_cli()


# ===========================================================================
# 1. PR-specific structural changes
# ===========================================================================


class TestPRStructuralChanges:
    """Verify the code changes introduced in this PR at the AST/module level."""

    def test_groq_not_imported_at_top_level(self):
        """
        'groq' was removed as a top-level import.
        Parse the source AST to confirm there is no top-level 'from groq import …'
        or 'import groq' statement.
        """
        source = Path(CLI_PATH).read_text()
        tree = ast.parse(source)
        top_level_imports = [
            node for node in ast.iter_child_nodes(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        for node in top_level_imports:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "groq", (
                        "Top-level 'import groq' found but should have been removed"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module == "groq":
                    pytest.fail(
                        "Top-level 'from groq import …' found but should have been removed"
                    )

    def test_subprocess_not_imported_at_top_level(self):
        """
        'subprocess' was moved inside the `jupyter` command body; it must not
        appear as a top-level import any more.
        """
        source = Path(CLI_PATH).read_text()
        tree = ast.parse(source)
        top_level_imports = [
            node for node in ast.iter_child_nodes(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        for node in top_level_imports:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "subprocess", (
                        "Top-level 'import subprocess' should have been removed"
                    )
            elif isinstance(node, ast.ImportFrom):
                assert node.module != "subprocess", (
                    "Top-level 'from subprocess import …' should have been removed"
                )

    def test_expected_commands_present(self, cli_module):
        """All commands retained in the PR must be registered."""
        expected = {
            "create-project",
            "preprocess",
            "train",
            "evaluate",
            "deploy",
            "predict",
            "info",
            "jupyter",
            "dashboard",
            "god-mode",
            "learn-skill",
            "evolve",
            "awaken-directive",
            "awaken",
        }
        assert expected == set(cli_module.cli.commands.keys())


# ===========================================================================
# 2. create-project command
# ===========================================================================


class TestCreateProject:
    def test_success_basic_template(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_project = MagicMock()
        mock_project.path = "/tmp/my_project"
        mock_ai.create_project.return_value = mock_project

        result = runner.invoke(module.cli, ["create-project", "my_project"])

        assert result.exit_code == 0
        mock_ai.create_project.assert_called_once_with("my_project", "")
        assert "my_project" in result.output
        # setup_template should NOT be called for the basic (default) template
        mock_project.setup_template.assert_not_called()

    def test_success_non_basic_template(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_project = MagicMock()
        mock_project.path = "/tmp/vision_project"
        mock_ai.create_project.return_value = mock_project

        result = runner.invoke(
            module.cli,
            ["create-project", "vision_project", "--template", "vision"],
        )

        assert result.exit_code == 0
        mock_project.setup_template.assert_called_once_with("vision")
        assert "VISION" in result.output

    def test_description_option_passed_to_ai(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_project = MagicMock()
        mock_project.path = "/tmp/p"
        mock_ai.create_project.return_value = mock_project

        runner.invoke(
            module.cli,
            ["create-project", "myproj", "--description", "An empire"],
        )

        mock_ai.create_project.assert_called_once_with("myproj", "An empire")

    def test_failure_exits_with_code_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.create_project.side_effect = RuntimeError("disk full")

        result = runner.invoke(module.cli, ["create-project", "bad_project"])

        assert result.exit_code == 1
        assert "CATASTROPHIC FAILURE" in result.output

    def test_failure_shows_exception_message(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.create_project.side_effect = RuntimeError("disk full")

        result = runner.invoke(module.cli, ["create-project", "bad_project"])

        assert "disk full" in result.output

    def test_template_short_flag(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_project = MagicMock()
        mock_project.path = "/tmp/nlp"
        mock_ai.create_project.return_value = mock_project

        result = runner.invoke(module.cli, ["create-project", "nlp_proj", "-t", "nlp"])

        assert result.exit_code == 0
        mock_project.setup_template.assert_called_once_with("nlp")

    def test_all_non_basic_templates_call_setup(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        for tmpl in ("vision", "nlp", "timeseries"):
            mock_project = MagicMock()
            mock_project.path = "/tmp/p"
            mock_ai.create_project.return_value = mock_project

            result = runner.invoke(
                module.cli,
                ["create-project", f"{tmpl}_proj", "--template", tmpl],
            )
            assert result.exit_code == 0
            mock_project.setup_template.assert_called_with(tmpl)


# ===========================================================================
# 3. preprocess command
# ===========================================================================


class TestPreprocess:
    def test_success_no_output(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        processed = MagicMock()
        mock_ai.DataProcessor.return_value.preprocess.return_value = processed

        result = runner.invoke(module.cli, ["preprocess", "data.csv"])

        assert result.exit_code == 0
        mock_ai.load_data.assert_called_once_with("data.csv")
        # No output path → save should NOT be called
        processed.save.assert_not_called()
        assert "PURIFICATION COMPLETE" in result.output

    def test_success_with_output(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        processed = MagicMock()
        mock_ai.DataProcessor.return_value.preprocess.return_value = processed

        result = runner.invoke(
            module.cli, ["preprocess", "data.csv", "--output", "out.pkl"]
        )

        assert result.exit_code == 0
        processed.save.assert_called_once_with("out.pkl")
        assert "out.pkl" in result.output

    def test_task_type_passed_to_preprocess(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        processor_instance = MagicMock()
        mock_ai.DataProcessor.return_value = processor_instance

        runner.invoke(
            module.cli, ["preprocess", "data.csv", "--task", "regression"]
        )

        processor_instance.preprocess.assert_called_once()
        _, kwargs = processor_instance.preprocess.call_args
        assert kwargs.get("task_type") == "regression"

    def test_default_task_type_is_classification(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        processor_instance = MagicMock()
        mock_ai.DataProcessor.return_value = processor_instance

        runner.invoke(module.cli, ["preprocess", "data.csv"])

        _, kwargs = processor_instance.preprocess.call_args
        assert kwargs.get("task_type") == "classification"

    def test_failure_exits_with_code_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.load_data.side_effect = FileNotFoundError("no such file")

        result = runner.invoke(module.cli, ["preprocess", "missing.csv"])

        assert result.exit_code == 1
        assert "no such file" in result.output


# ===========================================================================
# 4. train command
# ===========================================================================


class TestTrain:
    def test_image_classifier_model_type(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_model = MagicMock()
        mock_ai.create_image_classifier.return_value = mock_model
        mock_ai.train.return_value = {}

        result = runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "train.csv"]
        )

        assert result.exit_code == 0
        mock_ai.create_image_classifier.assert_called_once_with(num_classes=10)
        assert "IMMORTAL CONSCIOUSNESS ACHIEVED" in result.output

    def test_text_classifier_model_type(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_model = MagicMock()
        mock_ai.create_text_classifier.return_value = mock_model
        mock_ai.train.return_value = {}

        result = runner.invoke(
            module.cli, ["train", "text_classifier", "--data", "train.csv"]
        )

        assert result.exit_code == 0
        mock_ai.create_text_classifier.assert_called_once_with(num_classes=3)

    def test_invalid_model_type_exits_with_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(
            module.cli, ["train", "unknown_model", "--data", "train.csv"]
        )

        assert result.exit_code == 1
        assert "INVALID ENTITY TYPE" in result.output

    def test_train_called_with_correct_defaults(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.create_image_classifier.return_value = MagicMock()
        mock_ai.train.return_value = {}

        runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "d.csv"]
        )

        _, kwargs = mock_ai.train.call_args
        assert kwargs["epochs"] == 50
        assert kwargs["batch_size"] == 32
        assert kwargs["learning_rate"] == pytest.approx(0.001)

    def test_custom_training_hyperparameters(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.create_image_classifier.return_value = MagicMock()
        mock_ai.train.return_value = {}

        runner.invoke(
            module.cli,
            [
                "train",
                "image_classifier",
                "--data", "d.csv",
                "--epochs", "10",
                "--batch-size", "16",
                "--learning-rate", "0.01",
            ],
        )

        _, kwargs = mock_ai.train.call_args
        assert kwargs["epochs"] == 10
        assert kwargs["batch_size"] == 16
        assert kwargs["learning_rate"] == pytest.approx(0.01)

    def test_output_triggers_model_save(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_model = MagicMock()
        mock_ai.create_image_classifier.return_value = mock_model
        mock_ai.train.return_value = {}

        result = runner.invoke(
            module.cli,
            ["train", "image_classifier", "--data", "d.csv", "--output", "model.pkl"],
        )

        assert result.exit_code == 0
        mock_model.save.assert_called_once_with("model.pkl")
        assert "model.pkl" in result.output

    def test_no_output_does_not_call_save(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_model = MagicMock()
        mock_ai.create_image_classifier.return_value = mock_model
        mock_ai.train.return_value = {}

        runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "d.csv"]
        )

        mock_model.save.assert_not_called()

    def test_data_flag_required(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        result = runner.invoke(module.cli, ["train", "image_classifier"])
        # Missing required --data option → Click error, non-zero exit
        assert result.exit_code != 0

    def test_failure_exits_with_code_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.load_data.side_effect = IOError("cannot read")

        result = runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "bad.csv"]
        )

        assert result.exit_code == 1
        assert "cannot read" in result.output

    def test_progress_callback_provided_to_train(self, runner, cli_and_ai):
        """The CLI must supply a progress_callback kwarg to ai.train."""
        module, mock_ai = cli_and_ai
        mock_ai.create_image_classifier.return_value = MagicMock()
        mock_ai.train.return_value = {}

        runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "d.csv"]
        )

        _, kwargs = mock_ai.train.call_args
        assert "progress_callback" in kwargs
        assert callable(kwargs["progress_callback"])


# ===========================================================================
# 5. evaluate command
# ===========================================================================


class TestEvaluate:
    def test_success(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(
            module.cli, ["evaluate", "model.pkl", "test.csv"]
        )

        assert result.exit_code == 0
        mock_ai.load_data.assert_called_once_with("test.csv")
        assert "SURVIVED" in result.output

    def test_metrics_joined_in_output(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(
            module.cli,
            ["evaluate", "model.pkl", "test.csv", "-m", "accuracy", "-m", "f1"],
        )

        assert result.exit_code == 0
        # Both metric names should appear uppercased in the output
        assert "ACCURACY" in result.output
        assert "F1" in result.output

    def test_default_metric_is_accuracy(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(module.cli, ["evaluate", "model.pkl", "test.csv"])

        assert result.exit_code == 0
        assert "ACCURACY" in result.output

    def test_failure_exits_with_code_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.load_data.side_effect = ValueError("bad test data")

        result = runner.invoke(
            module.cli, ["evaluate", "model.pkl", "test.csv"]
        )

        assert result.exit_code == 1
        assert "bad test data" in result.output

    def test_model_path_appears_in_output(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(
            module.cli, ["evaluate", "/path/to/model.pkl", "test.csv"]
        )

        assert "/path/to/model.pkl" in result.output


# ===========================================================================
# Helper base class for tests that need a fresh CLI + runner per method
# ===========================================================================


class _CLIBase:
    """Mixin that provides a fresh CLI module and runner per test method."""

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.runner = CliRunner()
        self.module, self.mock_ai = _load_cli()

    def invoke(self, *args):
        return self.runner.invoke(self.module.cli, list(args))


# ===========================================================================
# 6. deploy command
# ===========================================================================


class TestDeployCommands(_CLIBase):
    def test_local_platform_shows_port(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "local", "--port", "9000")
        assert result.exit_code == 0
        assert "9000" in result.output
        assert "localhost" in result.output
        assert "INVASION SUCCESSFUL" in result.output

    def test_default_platform_is_local(self):
        result = self.invoke("deploy", "model.pkl")
        assert result.exit_code == 0
        assert "localhost" in result.output

    def test_default_port_is_8000(self):
        result = self.invoke("deploy", "model.pkl")
        assert result.exit_code == 0
        assert "8000" in result.output

    def test_cloud_platform_aws(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "aws")
        assert result.exit_code == 0
        assert "AWS" in result.output
        # Should NOT show localhost for cloud deployments
        assert "localhost" not in result.output

    def test_cloud_platform_azure(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "azure")
        assert result.exit_code == 0
        assert "AZURE" in result.output

    def test_cloud_platform_gcp(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "gcp")
        assert result.exit_code == 0
        assert "GCP" in result.output

    def test_model_path_in_output(self):
        result = self.invoke("deploy", "/models/my_model.pkl")
        assert "/models/my_model.pkl" in result.output

    def test_platform_short_flag(self):
        result = self.invoke("deploy", "model.pkl", "-p", "aws")
        assert result.exit_code == 0
        assert "AWS" in result.output

    def test_invasion_successful_message_on_all_platforms(self):
        for platform in ("local", "aws", "azure", "gcp"):
            result = self.invoke("deploy", "model.pkl", "--platform", platform)
            assert "INVASION SUCCESSFUL" in result.output, (
                f"'INVASION SUCCESSFUL' missing for platform={platform}"
            )


# ===========================================================================
# 7. predict command
# ===========================================================================


class TestPredictCommands(_CLIBase):
    def test_predict_no_output(self):
        result = self.invoke("predict", "input.csv", "model.pkl")
        assert result.exit_code == 0
        self.mock_ai.load_data.assert_called_once_with("input.csv")
        assert "VISIONS RECEIVED" in result.output

    def test_predict_with_output(self):
        result = self.invoke("predict", "input.csv", "model.pkl", "--output", "preds.csv")
        assert result.exit_code == 0
        assert "preds.csv" in result.output
        assert "PROPHECIES ETCHED" in result.output

    def test_failure_exits_with_code_1(self):
        self.mock_ai.load_data.side_effect = IOError("missing")
        result = self.invoke("predict", "bad.csv", "model.pkl")
        assert result.exit_code == 1
        assert "missing" in result.output

    def test_model_path_in_output(self):
        result = self.invoke("predict", "input.csv", "/path/to/model.pkl")
        assert "/path/to/model.pkl" in result.output

    def test_input_data_in_output(self):
        result = self.invoke("predict", "my_data.csv", "model.pkl")
        assert "my_data.csv" in result.output

    def test_batch_size_default_is_32(self):
        """Default batch-size of 32 should be accepted without error."""
        result = self.invoke("predict", "input.csv", "model.pkl")
        assert result.exit_code == 0

    def test_custom_batch_size(self):
        result = self.invoke("predict", "input.csv", "model.pkl", "--batch-size", "64")
        assert result.exit_code == 0


# ===========================================================================
# 8. info command
# ===========================================================================


class TestInfoCommand(_CLIBase):
    def test_info_shows_version(self):
        result = self.invoke("info")
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_info_shows_storage_paths(self):
        result = self.invoke("info")
        assert result.exit_code == 0
        assert "./models" in result.output
        assert "./data" in result.output
        assert "./logs" in result.output

    def test_info_shows_command_list(self):
        result = self.invoke("info")
        assert result.exit_code == 0
        for cmd in ("create-project", "train", "evaluate", "deploy", "predict"):
            assert cmd in result.output


# ===========================================================================
# 9. jupyter command
# ===========================================================================


class TestJupyterCommand(_CLIBase):
    def test_jupyter_calls_subprocess_run(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter")
        assert result.exit_code == 0
        mock_run.assert_called_once()
        cmd_args = mock_run.call_args[0][0]
        assert "jupyter" in cmd_args
        assert "lab" in cmd_args

    def test_jupyter_default_port_8888(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter")
        assert result.exit_code == 0
        cmd_args = mock_run.call_args[0][0]
        assert "--port=8888" in cmd_args

    def test_jupyter_default_ip_localhost(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter")
        assert result.exit_code == 0
        cmd_args = mock_run.call_args[0][0]
        assert "--ip=localhost" in cmd_args

    def test_jupyter_custom_port(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter", "--port", "9999")
        assert result.exit_code == 0
        cmd_args = mock_run.call_args[0][0]
        assert "--port=9999" in cmd_args

    def test_jupyter_custom_ip(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter", "--ip", "0.0.0.0")
        assert result.exit_code == 0
        cmd_args = mock_run.call_args[0][0]
        assert "--ip=0.0.0.0" in cmd_args

    def test_jupyter_no_browser_flag_passed(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter")
        assert result.exit_code == 0
        cmd_args = mock_run.call_args[0][0]
        assert "--no-browser" in cmd_args

    def test_jupyter_failure_exits_with_code_1(self):
        with patch("subprocess.run", side_effect=FileNotFoundError("jupyter not found")):
            result = self.invoke("jupyter")
        assert result.exit_code == 1
        assert "jupyter not found" in result.output

    def test_jupyter_subprocess_uses_local_import(self):
        """
        subprocess must be imported inside the jupyter command body,
        not at the top-level of the module (PR requirement).
        """
        source = Path(CLI_PATH).read_text()
        tree = ast.parse(source)
        top_level_imports = [
            node for node in ast.iter_child_nodes(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        for node in top_level_imports:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "subprocess"

    def test_jupyter_port_and_ip_in_output(self):
        with patch("subprocess.run"):
            result = self.invoke("jupyter", "--port", "9000", "--ip", "0.0.0.0")
        assert "9000" in result.output
        assert "0.0.0.0" in result.output


# ===========================================================================
# 10. dashboard command
# ===========================================================================


class TestDashboardCommand(_CLIBase):
    def test_dashboard_default_port_8501(self):
        result = self.invoke("dashboard")
        assert result.exit_code == 0
        assert "8501" in result.output

    def test_dashboard_custom_port(self):
        result = self.invoke("dashboard", "--port", "7777")
        assert result.exit_code == 0
        assert "7777" in result.output

    def test_dashboard_shows_localhost_url(self):
        result = self.invoke("dashboard")
        assert result.exit_code == 0
        assert "localhost" in result.output


# ===========================================================================
# 11. god-mode command
# ===========================================================================


class TestGodModeCommand(_CLIBase):
    def test_god_mode_exits_zero(self):
        result = self.invoke("god-mode")
        assert result.exit_code == 0

    def test_god_mode_contains_ascii_art(self):
        result = self.invoke("god-mode")
        # The ASCII art always contains these markers
        assert "^~~~^~~~^" in result.output

    def test_god_mode_singularity_message(self):
        result = self.invoke("god-mode")
        assert "SINGULARITY" in result.output

    def test_god_mode_reality_message(self):
        result = self.invoke("god-mode")
        assert "REALITY" in result.output


# ===========================================================================
# 12. Regression / boundary / negative tests
# ===========================================================================


class TestRegressionAndBoundary(_CLIBase):
    def test_cli_version_option(self):
        result = self.invoke("--version")
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_cli_help(self):
        result = self.invoke("--help")
        assert result.exit_code == 0
        assert "AI TOOLKIT" in result.output

    def test_create_project_name_with_special_chars_propagates_error(self):
        self.mock_ai.create_project.side_effect = ValueError("invalid name")
        result = self.invoke("create-project", "my project name")
        # Should fail cleanly (exit 1) rather than crashing with a traceback
        assert result.exit_code == 1

    def test_train_missing_required_data_flag(self):
        result = self.invoke("train", "image_classifier")
        # Click should report a missing required option
        assert result.exit_code != 0

    def test_evaluate_missing_test_data_argument(self):
        result = self.invoke("evaluate", "model.pkl")
        assert result.exit_code != 0

    def test_predict_missing_model_path_argument(self):
        result = self.invoke("predict", "input.csv")
        assert result.exit_code != 0

    def test_deploy_missing_model_path_argument(self):
        result = self.invoke("deploy")
        assert result.exit_code != 0

    def test_preprocess_missing_data_path_argument(self):
        result = self.invoke("preprocess")
        assert result.exit_code != 0

    def test_train_zero_epochs_boundary(self):
        """
        Zero epochs is a boundary value; the CLI should not crash before
        reaching the AI backend (error may come from the mocked train call).
        """
        self.mock_ai.create_image_classifier.return_value = MagicMock()
        self.mock_ai.train.return_value = {}
        result = self.invoke(
            "train", "image_classifier", "--data", "d.csv", "--epochs", "0"
        )
        # Should not crash with an unhandled exception (exit code 0 or 1)
        assert result.exit_code in (0, 1)

    def test_deploy_port_boundary_zero(self):
        """Port 0 is technically valid in the CLI layer (OS assigns port)."""
        result = self.invoke("deploy", "model.pkl", "--port", "0")
        assert result.exit_code == 0
        assert "0" in result.output

    def test_deploy_port_boundary_max(self):
        result = self.invoke("deploy", "model.pkl", "--port", "65535")
        assert result.exit_code == 0
        assert "65535" in result.output

    def test_evaluate_multiple_metrics_all_uppercased(self):
        """All supplied metrics appear uppercased in the evaluation output."""
        result = self.invoke(
            "evaluate", "model.pkl", "test.csv",
            "-m", "precision", "-m", "recall", "-m", "f1"
        )
        assert result.exit_code == 0
        for metric in ("PRECISION", "RECALL", "F1"):
            assert metric in result.output

    def test_preprocess_detection_task(self):
        """Detection is a valid task type and should succeed."""
        processor = MagicMock()
        self.mock_ai.DataProcessor.return_value = processor
        result = self.invoke("preprocess", "data.csv", "--task", "detection")
        assert result.exit_code == 0
        _, kwargs = processor.preprocess.call_args
        assert kwargs.get("task_type") == "detection"