from enum import Enum
import os
import platform
import warnings


class DATA_ANALYSIS_OPTIONS_ENUM(Enum):
    PANDAS = "pandas"
    POLARS = "polars"


DATA_ANALYSIS_OPTIONS = DATA_ANALYSIS_OPTIONS_ENUM.PANDAS

# Determine the operating system
os_type = platform.system()

__DEFAULT_TMP_FOLDER = "pluto_sdk"

# Set the temporary folder based on the OS
match os_type:
    case "Windows":
        DEFAULT_TMP_PATH = os.path.join(os.environ["TEMP"], "pluto_sdk")
    case "Darwin":
        DEFAULT_TMP_PATH = f"/private/var/folders/{__DEFAULT_TMP_FOLDER}"
    case "Linux":
        DEFAULT_TMP_PATH = f"/tmp/{__DEFAULT_TMP_FOLDER}"
    case _:
        warnings.warn(
            f"Unsupported operating system: {os_type}. Files will be save locally in a folder called {__DEFAULT_TMP_FOLDER}"
        )
        DEFAULT_TMP_PATH = __DEFAULT_TMP_FOLDER
