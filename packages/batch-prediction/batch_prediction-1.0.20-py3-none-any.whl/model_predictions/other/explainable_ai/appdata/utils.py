import numpy as np
import pandas as pd


def find_unique_values(input_array):
    """
            Method to find unique values from a given data column

            Args:
                input_array : array to find unique values of

            Returns:
                list of unique values
    """
    # check if instance of numpy or pandas

    testArray = input_array
    if isinstance(input_array,pd.core.frame.DataFrame):
        testArray = input_array.to_numpy()
    if isinstance(testArray, np.ndarray):
        unique_values = np.unique(testArray).tolist()
    elif isinstance(testArray, pd.core.series.Series):
        unique_values = testArray.unique().tolist()
        # unique_values = [x if any([isinstance(x,int),isinstance(x,float)]) else 0 for x in unique_values]
    else:
        unique_values = "Array Entered is neither Pandas Series df nor numpy array"
    return unique_values


def generate_predict_fn(model, mode="classification", preprocess_fn=None):
    """
        Method to generate predict function for a given model
    Args:
        model: model to generate predict function for
        mode: mode of the model
        preprocess_fn: preprocess function to be applied to the input data

    Returns: predict function

    """
    if mode == "classification":
        predict_fn = lambda x: model.predict_proba
    else:
        predict_fn = lambda x: model.predict
    return predict_fn


def generate_sample_request(x):
    """
        Method to generate sample request for a given input data
    Args:
        x: input data to generate sample request for

    Returns: sample request

    """
    # logger.info("Generating sample request for input data")
    if type(x) == np.ndarray:
        return x[0].tolist()
    elif type(x) == pd.core.series.Series:
        return x.iloc[0].tolist()
    else:
        return "Array Entered is neither Pandas Series df nor numpy array"
