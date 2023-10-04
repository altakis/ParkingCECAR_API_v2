import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the directory where log files will be stored
LOGGING_DIR = os.path.join(BASE_DIR, "logs")
isExist = os.path.exists(LOGGING_DIR)
if not isExist:
    os.makedirs(LOGGING_DIR)
