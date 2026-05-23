"""
Tests for ai_toolkit.py CLI.

This module tests the CLI commands defined in ai_toolkit.py, covering:
- Correct behaviour of all commands
- Error-handling paths (exception → sys.exit(1))
- Default option values
- Branching logic (deploy local vs cloud, train model types, template handling)
- Structural tests to ensure no heavy top-level imports
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
        "ai_toolkit.skills",
        "ai_toolkit.autonomy",
        "ai_toolkit.nlp",
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
    # CliRunner in this environment does not support mix_stderr
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
# 1. Structural changes
# ===========================================================================


class TestStructuralChanges:
    """Verify the code structure at the AST/module level."""

    def test_groq_not_imported_at_top_level(self):
        """
        'groq' must not be imported at the top level.
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
                        "Top-level 'import groq' found but should be lazy-loaded"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module == "groq":
                    pytest.fail(
                        "Top-level 'from groq import …' found but should be lazy-loaded"
                    )

    def test_subprocess_not_imported_at_top_level(self):
        """
        'subprocess' must not appear as a top-level import.
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
                        "Top-level 'import subprocess' found but should be lazy-loaded"
                    )
            elif isinstance(node, ast.ImportFrom):
                assert node.module != "subprocess", (
                    "Top-level 'from subprocess import …' found but should be lazy-loaded"
                )

    def test_expected_commands_present(self, cli_module):
        """All commands must be registered."""
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
        assert expected.issubset(set(cli_module.cli.commands.keys()))


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
        assert "IMMORTAL CONSCIOUSNESS" in result.output

    def test_invalid_model_type_exits_with_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai

        result = runner.invoke(
            module.cli, ["train", "unknown_model", "--data", "train.csv"]
        )

        assert result.exit_code == 1
        assert "INVALID ENTITY TYPE" in result.output

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

    def test_failure_exits_with_code_1(self, runner, cli_and_ai):
        module, mock_ai = cli_and_ai
        mock_ai.load_data.side_effect = IOError("cannot read")

        result = runner.invoke(
            module.cli, ["train", "image_classifier", "--data", "bad.csv"]
        )

        assert result.exit_code == 1
        assert "cannot read" in result.output


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
# 5. evaluate command
# ===========================================================================


class TestEvaluateCommands(_CLIBase):
    def test_success(self):
        result = self.invoke("evaluate", "model.pkl", "test.csv")
        assert result.exit_code == 0
        assert "SURVIVED" in result.output

    def test_failure_exits_with_code_1(self):
        self.mock_ai.load_data.side_effect = ValueError("bad test data")
        result = self.invoke("evaluate", "model.pkl", "test.csv")
        assert result.exit_code == 1
        assert "bad test data" in result.output


# ===========================================================================
# 6. deploy command
# ===========================================================================


class TestDeployCommands(_CLIBase):
    def test_local_platform_shows_port(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "local", "--port", "9000")
        assert result.exit_code == 0
        assert "9000" in result.output
        assert "INVASION SUCCESSFUL" in result.output

    def test_cloud_platform_aws(self):
        result = self.invoke("deploy", "model.pkl", "--platform", "aws")
        assert result.exit_code == 0
        assert "AWS" in result.output


# ===========================================================================
# 7. predict command
# ===========================================================================


class TestPredictCommands(_CLIBase):
    def test_predict_no_output(self):
        result = self.invoke("predict", "input.csv", "model.pkl")
        assert result.exit_code == 0
        assert "VISIONS RECEIVED" in result.output


# ===========================================================================
# 8. info command
# ===========================================================================


class TestInfoCommand(_CLIBase):
    def test_info_shows_version(self):
        result = self.invoke("info")
        assert result.exit_code == 0
        assert "1.0.0" in result.output


# ===========================================================================
# 9. jupyter command
# ===========================================================================


class TestJupyterCommand(_CLIBase):
    def test_jupyter_calls_subprocess_run(self):
        with patch("subprocess.run") as mock_run:
            result = self.invoke("jupyter")
        assert result.exit_code == 0
        mock_run.assert_called_once()

    def test_jupyter_failure_exits_with_code_1(self):
        with patch("subprocess.run", side_effect=FileNotFoundError("jupyter not found")):
            result = self.invoke("jupyter")
        assert result.exit_code == 1
        assert "jupyter not found" in result.output


# ===========================================================================
# 10. dashboard command
# ===========================================================================


class TestDashboardCommand(_CLIBase):
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
        assert "^~~~^~~~^" in result.output


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

    def test_awaken_command_exists(self):
        """
        Verify that 'awaken' command exists and can be invoked.
        """
        # We mock Groq since it's used in awaken
        with patch("groq.Groq"):
            result = self.invoke("awaken")
            # It might fail due to lack of input, but should exist
            assert result.exit_code != 2 # 2 means command not found

    def test_awaken_in_help_output(self):
        """The 'awaken' command should appear in --help output."""
        result = self.invoke("--help")
        assert "awaken" in result.output
