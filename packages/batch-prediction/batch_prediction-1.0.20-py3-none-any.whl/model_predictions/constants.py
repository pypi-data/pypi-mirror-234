import os

BASE_DIR = os.getcwd()




class ModelConstants:
    MODEL_DIR = os.path.join(BASE_DIR, "datasource")
    MODEL_FILE = "ml_model"
    SCORING_FUN = "scoring_func"
    MODELS_PATH = "/models"


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


class CRANPackageList:
    pre_installed_packages = [
        "base",
        "boot",
        "class",
        "cluster",
        "codetools",
        "compiler",
        "datasets",
        "evaluate",
        "foreign",
        "graphics",
        "grDevices",
        "grid",
        "IRkernel",
        "KernSmooth",
        "lattice",
        "MASS",
        "Matrix",
        "methods",
        "mgcv",
        "mosaicrml",
        "nlme",
        "nnet",
        "parallel",
        "pbdZMQ",
        "compareDF",
        "rlang",
        "rpart",
        "spatial",
        "splines",
        "stats",
        "stats4",
        "survival",
        "tcltk",
        "tools",
        "utils",
    ]


class Model:
    flavour = "MODEL_FLAVOUR"
    directory = "MODEL_DIRECTORY"
    download_url = "MODEL_DOWNLOAD_URL"
    init_script = "MODEL_INIT_SCRIPT"
    model_file = "ml_model"
    r_model_file = "model.rds"
    scoring_func_file = "scoring_func"
    r_scoring_func_file = "score.rds"
    input_type = "INPUT_TYPE"
    x_train_func_file = "x_train"
    model_list_file = "model_list"
    deployment_strategy = "DEPLOYMENT_STRATEGY"
    deployment_id = "DEPLOYMENT_ID"
    deployment_data = "DEPLOYMENT_DATA"
    scoring_func_file_sas = "score_func.sas"
    custom_predict_file = "custom_score"
    source = "SOURCE"


class ModelSource:
    mlflow = "mlflow"
