import os.path
from pathlib import Path

""" Build paths inside the project like this: BASE_DIR / "subdir".
The first .parent identifies the current folder.
The second creates a path to the parent directory in this case core.
The third and final points to the project root folder.
If this was a module file instead of a module package then only
two calls of .parent would have been enough.
"""
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define the directory where log files will be stored
LOGGING_DIR = os.path.join(BASE_DIR, "logs")
isExist = os.path.exists(LOGGING_DIR)
if not isExist:
    os.makedirs(LOGGING_DIR)
