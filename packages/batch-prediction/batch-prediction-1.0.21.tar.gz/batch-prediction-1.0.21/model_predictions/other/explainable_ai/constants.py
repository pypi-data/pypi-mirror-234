import os
from typing import Final

BASE_DIR = os.getcwd()

class ModelConstants:
    MODEL_DIR: Final = os.path.join(BASE_DIR,"datasource")
    MODEL_FILE: Final = "ml_model"
    X_TRAIN: Final = "x_train"
    X_TEST: Final = "x_test"
    Y_TRAIN: Final = "y_train"
    Y_TEST: Final = "y_test"
    SCORING_FUN: Final = "scoring_func"
    Reverse_Map: Final = "label_map"
    Meta_Info: Final = "meta_info"
    Requirments: Final = "requirement"


class Flavour:
    keras = "keras"
    sklearn = "sklearn"
    pytorch = "pytorch"
    tensorflow = "tensorflow"
    pyspark = "pyspark"
    spacy = "spacy"
    r = "r"
    pmml = "pmml"
    ensemble = "ensemble"
    sas = "sas"
    xgboost = "xgboost"