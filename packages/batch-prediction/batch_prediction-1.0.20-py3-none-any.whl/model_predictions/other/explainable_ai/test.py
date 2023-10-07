

import cloudpickle
import pandas as pd

if __name__ == "__main__":
    import pathlib,shutil
    for i in pathlib.Path(".").rglob("__pycache__"):
        shutil.rmtree(i)