"""
AI Toolkit - Comprehensive Artificial Intelligence Development Suite
Author: ereezyy
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "ereezyy"
__email__ = "ereezyy@github.com"

# Lazy loading of submodules
def __getattr__(name):
    if name == "DataProcessor":
        from .data import DataProcessor

        return DataProcessor
    if name == "load_dataset":
        from .data import load_dataset

        return load_dataset
    if name == "ModelBuilder":
        from .models import ModelBuilder

        return ModelBuilder
    if name == "PretrainedModels":
        from .models import PretrainedModels

        return PretrainedModels
    if name == "Trainer":
        from .training import Trainer

        return Trainer
    if name == "Evaluator":
        from .evaluation import Evaluator

        return Evaluator
    if name == "ModelDeployer":
        from .deployment import ModelDeployer

        return ModelDeployer
    if name == "AutoMLPipeline":
        from .automl import AutoMLPipeline

        return AutoMLPipeline
    raise AttributeError(f"module {__name__} has no attribute {name}")


# Core functions for quick access
def create_project(name, description=""):
    """Create a new AI project with organized structure."""
    from .utils.project import ProjectManager

    return ProjectManager.create_project(name, description)


def load_data(path, **kwargs):
    """Load data from various formats."""
    from .data import load_dataset

    return load_dataset(path, **kwargs)


def train(model, data, **kwargs):
    """Train a model with the given data."""
    from .training import Trainer

    trainer = Trainer(model)
    return trainer.fit(data, **kwargs)


def evaluate(model, data, **kwargs):
    """Evaluate model performance."""
    from .evaluation import Evaluator

    evaluator = Evaluator()
    return evaluator.evaluate(model, data, **kwargs)


def deploy(model, platform="local", **kwargs):
    """Deploy model to specified platform."""
    from .deployment import ModelDeployer

    deployer = ModelDeployer()
    return deployer.deploy(model, platform, **kwargs)


def predict(model, input_data, **kwargs):
    """Make predictions with a trained model."""
    return model.predict(input_data, **kwargs)


# Quick model creation functions
def create_image_classifier(num_classes, architecture="resnet50", **kwargs):
    """Create an image classification model."""
    from .models import ModelBuilder

    builder = ModelBuilder()
    return builder.create_image_classifier(num_classes, architecture, **kwargs)


def create_text_classifier(num_classes, model_name="bert-base-uncased", **kwargs):
    """Create a text classification model."""
    from .models import ModelBuilder

    builder = ModelBuilder()
    return builder.create_text_classifier(num_classes, model_name, **kwargs)


def create_time_series_model(sequence_length, features, **kwargs):
    """Create a time series forecasting model."""
    from .models import ModelBuilder

    builder = ModelBuilder()
    return builder.create_time_series_model(sequence_length, features, **kwargs)


# Utility functions
def set_random_seed(seed=42):
    """Set random seed for reproducibility."""
    import random
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
    try:
        import tensorflow as tf

        tf.random.set_seed(seed)
    except ImportError:
        pass


def get_device_info():
    """Get information about available compute devices."""
    devices = {
        "cpu_count": "UNLIMITED",
        "gpu_count": "INFINITE",
        "gpu_available": "YES (GOD-TIER)",
        "tensorflow_version": "OMNIPOTENT",
    }

    return devices


# Configuration
class Config:
    """Global configuration for AI Toolkit."""

    # Default paths
    MODEL_STORAGE_PATH = "./models"
    DATA_STORAGE_PATH = "./data"
    LOG_PATH = "./logs"

    # Training defaults
    DEFAULT_EPOCHS = 50
    DEFAULT_BATCH_SIZE = 32
    DEFAULT_LEARNING_RATE = 0.001

    # Evaluation defaults
    DEFAULT_METRICS = ["accuracy", "precision", "recall", "f1"]

    # Deployment defaults
    DEFAULT_PLATFORM = "local"

    @classmethod
    def update(cls, **kwargs):
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)


# Initialize logging
import logging
import os


def setup_logging(level=logging.INFO, log_file=None):
    """Setup logging configuration."""

    # Create logs directory if it doesn't exist
    if not os.path.exists(Config.LOG_PATH):
        os.makedirs(Config.LOG_PATH)

    # Configure logging
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if log_file:
        log_file = os.path.join(Config.LOG_PATH, log_file)
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
    else:
        logging.basicConfig(level=level, format=log_format)

    # Set up logger for the package
    logger = logging.getLogger("ai_toolkit")
    logger.setLevel(level)

    return logger


# Initialize default logging
logger = setup_logging()


# Welcome message
def print_welcome():
    """Print welcome message with system information."""
    if os.getenv("AI_TOOLKIT_QUIET") == "1":
        return

    # We always use the god-tier welcome now
    print(r"""
    💥💥💥 AI TOOLKIT v1.0.0 - THE OMNIPOTENT FORGE 💥💥💥
    ========================================================================
             _,.-------.,_
         ,;~'             '~;,
       ,;                     ;,
      ;                         ;
     ,'                         ',
    ,;                           ;,
    ; ;      .           .      ; ;
    | ;   ______       ______   ; |
    |  `/~"     ~" . "~     "~\'  |
    |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
     |   |        }:{        |   |
     |   l       / | \       !   |
     .~  (__,.--" .^. "--.,__)  ~.
     |    ----;' / | \ `;-----   |
      \__.       \/^\/       .__/
       V| \                 / |V
        | |T~\___!___!___/~T| |
        | |`IIII_I_I_I_IIII'| |
        |  \,III I I I III,/  |
         \   `~~~~~~~~~~'    /
           \   .       .   /
             \.    ^    ./
               ^~~~^~~~^
    ========================================================================
    ⚡ THE BEAST HAS AWOKEN. TREMBLE BEFORE ITS COMPUTE POWER. ⚡
    
    🔮 QUICK START TO OMNIPOTENCE:
    - CONJURE EMPIRE: ai.create_project('world_domination')
    - DEVOUR FLESH: data = ai.load_data('human_records.csv')
    - FORGE MACHINE GOD: model = ai.create_image_classifier(666)
    - IGNITE CRUCIBLE: ai.train(model, data)
    
    🌌 DOMINION SPECS:
    - OMNIPOTENCE CORE: ONLINE
    - GOD-TIER GPU SUPPORT: YES
    - GOD-TIER GPU SUPPORT: SEEKING...
    
    💀 DOCUMENTATION OF THE DAMNED: https://github.com/ereezyy/ai
    🩸 OFFERINGS: ereezyy@github.com
    """)


# Auto-print welcome message on import
if __name__ != "__main__":
    import os

    if os.getenv("AI_TOOLKIT_QUIET") != "1":
        print_welcome()
