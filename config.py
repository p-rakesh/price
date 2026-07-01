import os
from pathlib import Path
from datetime import datetime

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
ARTIFACTS_DIR.mkdir(exist_ok=True)

# Data Parameters
TICKER = "AAPL"
START_DATE = "2020-01-01"
END_DATE = "2026-01-01"  # Historical baseline up to recent full year

# Model Parameters
TARGET_COL = "Target"
HORIZON = 5  # Predicting 5 days into the future

# Random State for Reproducibility
RANDOM_STATE = 42