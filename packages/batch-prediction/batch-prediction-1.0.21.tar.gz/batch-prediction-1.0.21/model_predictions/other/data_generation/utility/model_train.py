import os, json, ast, re
from typing import Final
from path import Path
from pandas import DataFrame
from refractio import get_local_dataframe
from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from ydata_synthetic.synthesizers import ModelParameters, TrainParameters
from ydata_profiling import ProfileReport
from evidently.options import ColorOptions

directory = Path(__file__).abspath()
COLOR_CODE_FEATURE : Final = 'feature'


def get_custom_colors(type=COLOR_CODE_FEATURE):
    if type == COLOR_CODE_FEATURE:
        color_scheme = ColorOptions()
        color_scheme.primary_color = "#7634B1" # HISTOGRAM
        color_scheme.fill_color = "#E8E1F0" # STANDARD DEV BACKGROUND
        color_scheme.zero_line_color = "#7634B1" #MEAN LINE
        color_scheme.current_data_color = "#007CFF" #CURRENT
        color_scheme.reference_data_color = "#4CAF50" #REFERENCE
        return color_scheme
    else:
        return None


def fetch_and_clean_data(path: str):
    data = get_local_dataframe(path)
    data = data.dropna()
    return data


def get_numerical_and_categorical_col(data: DataFrame, numerical: str, categorical: str):
    # Generating the standard profiling report
    profile = ProfileReport(data)
    json_profile = profile.to_json()
    new_profile = json.loads(json_profile)
    if numerical == 'auto':
        numerical_columns = [col for col, val in new_profile['variables'].items() if val['type'] == 'Numeric']
    elif ',' in numerical:
        pattern = re.compile('\'(.*?)\'')
        numerical_columns = pattern.findall(numerical)
    else:
        numerical_columns = []

    if categorical == 'auto':
        categorical_columns = [col for col, val in new_profile['variables'].items() if val['type']=='Categorical']
    elif ',' in categorical:
        pattern = re.compile('\'(.*?)\'')
        categorical_columns = pattern.findall(categorical)
    else:
        categorical_columns = []

    boolean_columns = [col for col, val in new_profile['variables'].items() if val['type'] == 'Boolean']

    return numerical_columns, categorical_columns, boolean_columns


def set_hyperparameters(epoch: str, learning_rate: str):
    ## Setting the architecture hyperparameters
    noise_dim = 32
    dim = 128
    batch_size = 64

    # Defined as per the literature on CWGAN
    beta_1 = 0.5
    beta_2 = 0.9

    log_step = 100
    epochs = ast.literal_eval(epoch)
    learning_rate = float(learning_rate)
    model_parameters = ModelParameters(batch_size=batch_size,
                                       lr=learning_rate,
                                       betas=(beta_1, beta_2),
                                       noise_dim=noise_dim,
                                       layers_dim=dim)

    train_args = TrainParameters(epochs=epochs,
                                 cache_prefix='',
                                 sample_interval=log_step,
                                 label_dim=-1,
                                 labels=(0, 1))
    return model_parameters, train_args


def train_model(data: DataFrame, model_parameters: ModelParameters, train_args: TrainParameters, numerical_columns: list, categorical_columns: list):
    synth = RegularSynthesizer(modelname='wgangp', model_parameters=model_parameters)

    # Model training
    synth.fit(data=data,
              train_arguments=train_args,
              num_cols=numerical_columns, cat_cols=categorical_columns)
    return synth


def train_conditional(data: DataFrame, model_parameters: ModelParameters, train_args: TrainParameters, numerical_columns: list, categorical_columns: list, label_columns: list):
    synth = RegularSynthesizer(modelname='cwgangp', model_parameters=model_parameters, n_critic=5)

    # Model training
    synth.fit(data=data,
              train_arguments=train_args,
              num_cols=numerical_columns, cat_cols=categorical_columns, label_cols=label_columns)
    return synth
