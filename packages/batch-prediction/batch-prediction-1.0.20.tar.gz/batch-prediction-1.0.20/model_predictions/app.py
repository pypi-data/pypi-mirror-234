import os
import inspect
from constants import ModelConstants, Flavour, Model, CRANPackageList, ModelSource
from utils import download_model, get_loader

from mosaic_utils.ai.file_utils import pickle_loads
from refractio import get_dataframe


def main():
    global model, scoring_func, model_info, application, scoring, model_dict, scoring_ensemble, use_score_v2, flavour
    model = None
    scoring_func = None
    scoring = None
    model_info = {}
    model_dict = {}
    scoring_ensemble = None
    use_score_v2 = False
    sas_session = None

    flavour = os.getenv(Model.flavour)
    input_file = "/data/" + os.getenv("reference_data_path")
    output_path = "/data/" + os.getenv("output_data_path", "prediction.csv")
    source = os.getenv("data_source")
    write_strategy = os.getenv("write_strategy")
    # flavour = "sklearn"
    # input_file = "models/fifa.csv"
    # output_path = "models/fifa_1.csv"

    model_tar_path = ModelConstants.MODELS_PATH
    print("******************")
    print("model_path", model_tar_path)
    print("model_flavour", flavour)
    print("input_file", input_file)
    print("output_path", output_path)
    print("source", source)
    print("write_strategy - ", write_strategy)
    print("******************")

    try:
        model_dir = download_model(model_tar_path)

        # model_file = os.path.join(model_path, ModelConstants.MODEL_FILE)
        # scoring_func_file = os.path.join(model_path, ModelConstants.SCORING_FUN)

        loader = get_loader(flavour) if flavour != Flavour.ensemble else ""

        # model = loader(model_file)
        # scoring_func = pickle_loads(scoring_func_file)

        if flavour == "r":
            # R import specifically moved below as it will give error of rpy2 while deploying otherwise
            from mosaic_utils.ai.flavours.r import (
                load_model,
                get_r_packages,
                load_r_packages,
                check_pre_installed_packages,
            )

            model_file = os.path.join(model_dir, Model.r_model_file)
            scoring_func_file = os.path.join(model_dir, Model.r_scoring_func_file)
            model = loader(model_file)
            scoring = loader(scoring_func_file)
            package_list, version_list = get_r_packages()
            cran_package_list = CRANPackageList.pre_installed_packages
            pkg_list = check_pre_installed_packages(
                package_list, version_list, cran_package_list
            )
            p_list = [package["name"] for package in pkg_list]
            load_r_packages(p_list)

        elif flavour == Flavour.sas:
            import saspy

            scoring_func = os.path.join(model_dir, Model.scoring_func_file_sas)
            sas_session = saspy.SASsession(results="HTML")
        else:
            if os.getenv("SOURCE") == ModelSource.mlflow:
                model_file = os.path.join(model_dir, "model.pkl")
                scoring_func_dir = os.path.dirname(model_dir)
                scoring_func_file = os.path.join(scoring_func_dir, "scoring_func")
                model = loader(model_file)
                scoring_func = pickle_loads(scoring_func_file)
            else:
                model_file = os.path.join(model_dir, Model.model_file)
                scoring_func_file = os.path.join(model_dir, Model.scoring_func_file)
                x_train_func_file = os.path.join(model_dir, Model.x_train_func_file)
                if os.path.exists(x_train_func_file):
                    x_train = pickle_loads(x_train_func_file)
                    # model_id, version_id, _ = os.environ["MODEL_DOWNLOAD_URL"].split("/")
                if model is None:
                    model = loader(model_file)
                    # scoring_func = pickle_loads(scoring_func_file)
                # if scoring_func and inspect.isclass(scoring_func):
                #     use_score_v2, scoring_func = True, scoring_func()

    except Exception as error:
        print("Error occurred ", error)

    if source.lower() == 'local data files':
        data, result = file_prediction(model, input_file)
        write_result(data, result, write_strategy, output_path)
    if source.lower() == 'refract datasets':
        db_prediction(model, scoring_func)

    ##################################
    # import time
    # print("Slee start")
    # time.sleep(120)
    # print("Slee end")

    # send notification send notification send notification send notification


def file_prediction(model, input_file):
    import pandas as pd
    import joblib

    # Step 1: Read the CSV file
    data = pd.read_csv(input_file)

    # Step 2: Load the pre-trained model
    model = model

    # Step 3: Create an empty list to store predictions
    predictions = []

    # Step 4: Iterate through each row and make predictions
    # for index, row in data.iterrows():
    #     # Assuming 'features' is the name of the input features used for prediction
    #     features = row[column_names].values  # Replace with your feature names
    #     prediction = model.predict(features[-16:])
    #     predictions.append(prediction[0])  # Append the prediction to the list

    # OR Step 4: make predictions
    predictions = model.predict(data)

    print("predictions", predictions)
    print("predictions type", type(predictions))
    print("data, predictions -", data, predictions)

    return data, predictions


def write_result(data, predictions, write_strategy, output_path):
    print("inside write_result write_result write_result write_result", write_strategy, output_path)
    # Step 5: Create a new DataFrame with the predictions

    # same_file data + result
    if write_strategy == 'Same':
        data['Prediction'] = predictions
        data.to_csv(output_path, index=False)
    # new_file with result only
    if write_strategy == 'New':
        print("save_method new", write_strategy, output_path)
        import numpy as np
        np.savetxt(output_path, predictions, header="Prediction")
        np.savetxt("savetxt.csv", np.dstack((np.arange(1, predictions.size + 1), predictions))[0],
                   "%d,%d", header="Id, Prediction")
    # if write_strategy == 'predictions':
    #     output_data = pd.DataFrame({'Prediction': predictions})
    #     output_data.to_csv(output_path, index=False)


def db_prediction(model, scoring_func):
    # read db_configs
    # conect to db
    # read data
    # run predictions
    # write predictions to db
    # send notification

    print(f"reading {os.getenv('reference_data_path')} with filter_condition: {os.getenv('filter_condition')}")
    data = get_dataframe(os.getenv('reference_data_path'),
                         filter_condition=os.getenv('filter_condition'))
    print(f"data read from refract dataset using refractio,"
          f"data.head(3): {data.head(3)}\ndata.shape: {data.shape}")
    data.dropna()

    column_names = data.columns.tolist()

    # Step 2: Load the pre-trained model
    model = model

    # Step 3: Create an empty list to store predictions
    predictions = []

    # Step 4: Iterate through each row and make predictions
    for index, row in data.iterrows():
        # Assuming 'features' is the name of the input features used for prediction
        features = row[column_names].values  # Replace with your feature names
        prediction = model.predict(features[-16:])
        predictions.append(prediction[0])  # Append the prediction to the list

    # Step 5: Create a new DataFrame with the predictions
    save_method = None
    if save_method == 'same_file':
        data['Predictions'] = predictions
        data.to_csv(input_file, index=False)
    if save_method == 'new_file':
        data['Predictions'] = predictions
        data.to_csv("output_predictions.csv", index=False)
    if save_method == 'predictions':
        output_data = pd.DataFrame({'Prediction': predictions})
        output_data.to_csv("predictions.csv", index=False)

    output_filename = 'data_generated_' + os.getenv('reference_data_path') + ".csv"
    return "OK"


if __name__ == "__main__":
    main()
