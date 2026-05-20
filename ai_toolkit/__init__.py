"""
AI Toolkit - Comprehensive Artificial Intelligence Development Suite
Author: ereezyy
Version: 1.0.0
License: MIT
"""

import sys
import os
import logging

__version__ = "1.0.0"
__author__ = "ereezyy"
__email__ = "ereezyy@github.com"

# Lazy loading of sub-modules
def __getattr__(name):
    if name in [
        "DataProcessor", "load_dataset", "ModelBuilder", "PretrainedModels",
        "Trainer", "Evaluator", "ModelDeployer", "AutoMLPipeline"
    ]:
        if name in ["DataProcessor", "load_dataset"]:
            from . import data
            return getattr(data, name)
        elif name in ["ModelBuilder", "PretrainedModels"]:
            from . import models
            return getattr(models, name)
        elif name == "Trainer":
            from . import training
            return getattr(training, name)
        elif name == "Evaluator":
            from . import evaluation
            return getattr(evaluation, name)
        elif name == "ModelDeployer":
            from . import deployment
            return getattr(deployment, name)
        elif name == "AutoMLPipeline":
            from . import automl
            return getattr(automl, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


# Core functions for quick access
def create_project(name, description=""):
    """Create a new AI project with organized structure."""
    from .utils.project import ProjectManager

    return ProjectManager.create_project(name, description)


def load_data(path, **kwargs):
    """Load data from various formats."""
    # Access via sys.modules to trigger __getattr__ or get the already loaded attribute
    return getattr(sys.modules[__name__], "load_dataset")(path, **kwargs)


def train(model, data, **kwargs):
    """Train a model with the given data."""
    Trainer = getattr(sys.modules[__name__], "Trainer")
    trainer = Trainer(model)
    return trainer.fit(data, **kwargs)


def evaluate(model, data, **kwargs):
    """Evaluate model performance."""
    Evaluator = getattr(sys.modules[__name__], "Evaluator")
    evaluator = Evaluator()
    return evaluator.evaluate(model, data, **kwargs)


def deploy(model, platform="local", **kwargs):
    """Deploy model to specified platform."""
    ModelDeployer = getattr(sys.modules[__name__], "ModelDeployer")
    deployer = ModelDeployer()
    return deployer.deploy(model, platform, **kwargs)


def predict(model, input_data, **kwargs):
    """Make predictions with a trained model."""
    return model.predict(input_data, **kwargs)


# Quick model creation functions
def create_image_classifier(num_classes, architecture="resnet50", **kwargs):
    """Create an image classification model."""
    ModelBuilder = getattr(sys.modules[__name__], "ModelBuilder")
    builder = ModelBuilder()
    return builder.create_image_classifier(num_classes, architecture, **kwargs)


def create_text_classifier(num_classes, model_name="bert-base-uncased", **kwargs):
    """Create a text classification model."""
    ModelBuilder = getattr(sys.modules[__name__], "ModelBuilder")
    builder = ModelBuilder()
    return builder.create_text_classifier(num_classes, model_name, **kwargs)


def create_time_series_model(sequence_length, features, **kwargs):
    """Create a time series forecasting model."""
    ModelBuilder = getattr(sys.modules[__name__], "ModelBuilder")
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
    if os.getenv("AI_TOOLKIT_QUIET") != "1":
        print_welcome()
