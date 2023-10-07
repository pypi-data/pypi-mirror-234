import os,json,re
from typing import Final
# from evidently.dashboard import Dashboard
# from evidently.dashboard.tabs import (DataDriftTab, CatTargetDriftTab, ProbClassificationPerformanceTab,
#         ClassificationPerformanceTab, NumTargetDriftTab, RegressionPerformanceTab)
# base = "/home/pcadmin/data/Mosaic/AIL/Projects/Snowflake/Streamlit/Drift/"
from path import Path
from evidently.report import Report
from evidently.metric_preset import  TargetDriftPreset
from evidently.options import ColorOptions
from evidently.metric_preset import TargetDriftPreset,ClassificationPreset,DataDriftPreset,RegressionPreset
from evidently.metric_preset import *
from pandas import DataFrame
from evidently.metrics import *
from utility.constants import ProblemType
directory = Path(__file__).abspath()

# from evidently.options import ColorOptions

COLOR_CODE_FEATURE : Final = 'feature'
def get_custom_colors(type=COLOR_CODE_FEATURE):

    color_scheme = ColorOptions()
    # color_scheme.primary_color = "#7BB5D9" # HISTOGRAM
    # color_scheme.fill_color = "#ffffff" # STANDARD DEV BACKGROUND
    # color_scheme.zero_line_color = "#887BD9" #MEAN LINE
    # color_scheme.current_data_color = "#D1906E" #CURRENT
    # color_scheme.reference_data_color = "#7BB5D9" #REFERENCE


    return color_scheme
    
    
def get_alert_configurations(recipe_name):
    alert_configuration = []
    
    # alert_env_info = os.getenv("alert_configuration")
    alert_info = json.loads(os.getenv("alert_configuration"))
    # print(alert_info)
    for metric_info in alert_info:
        parameter_name = [item["field_value"] for item in metric_info if item["field_id"]=="parameter"][0]
        max_value = [item["field_value"] for item in metric_info if item["field_id"]=="max_threshold"][0]
        min_value = [item["field_value"] for item in metric_info if item["field_id"]=="min_threshold"][0]
        severity = [item["field_value"] for item in metric_info if item["field_id"]=="severity"][0]

        temp_dict = {
                "parameter": parameter_name,
                "max_value": max_value,
                "min_value": min_value,
                "severity": severity
            }
        alert_configuration.append(temp_dict)
    
    return alert_configuration

def get_plugin_name():
    try:
        plugin_info = json.loads(os.getenv("plugin"))
        plugin_name = [item["field_value"] for item in plugin_info  if item['field_id']=="plugin_type"][0]
    except Exception as msg:
        print("Unable to load plugin name - error :",msg)
        raise Exception("Failed to load plugin env")
    
    return plugin_name

def update_alert_info(alert_data):
    model_name = None; model_id = None; version_no = None; plugin_name = None;version_id = None ; refract_source = None
    workflow_id = None ; plugin_id = None

    plugin_name = get_plugin_name()
    temp = alert_data["alert_data"]
    temp['recipe'] = plugin_name

    try:
        model_config = json.loads(os.getenv("model_configuration"))
        refract_source = model_config[0]["refract_source"]
        if refract_source == "model":
            model_name = [item["field_value"] for item in model_config if item['field_id']=="model_name"][0]
            model_id = [item["field_value"] for item in model_config if item['field_id']=="model_id"][0]
            version_no = [item["field_value"] for item in model_config if item['field_id']=="version_no"][0]
            version_id = [item["field_value"] for item in model_config if item['field_id']=="version_id"][0]
            temp_data = {
                    "description": {
                            "version": str(version_no)
                        },
                    "name": str(model_name),
                    "id": '_'.join([model_id,version_id]),
                    # "type" : "model"
                }
        elif refract_source == "workflow":
            workflow_id = [item["field_value"] for item in model_config if item['field_id']=="workflow_id"][0]
            plugin_id = [item["field_value"] for item in model_config if item['field_id']=="plugin_id"][0]
            temp_data = {
                    "description": {
                            "version": str(plugin_id)
                        },
                    "name": plugin_name,
                    "id": '_'.join([workflow_id,plugin_id]),
                    # "type" : "workflow"
                }

    except Exception as msg:
        print("Unable to load model_configurations - error :",msg)
        raise Exception("Failed to load env variables")

    temp.update({"object_metadata":temp_data})

    alert_data["alert_data"] =  temp

    print("Alert Info : \n",alert_data)
    
    return alert_data

def validate_inputs(temp):
    for item in temp:
        if not all([any([
                        isinstance(item[0],int),
                        isinstance(item[0],float),
                        ]),
                    any([
                        isinstance(item[1],int),
                        isinstance(item[1],float),
                        ])
                    ]
                    ):
            raise Exception("Alert thresholds should of type int or float")
        
        if not all([0 <= item[0] <= 1,0 <= item[1] <= 1]):
            raise Exception("threshold input range should be between 0 and 1")

def check_metric_status(alert_info,metric_value,parameter):
    # Severity Check
    drift_status = None 
    serverity_maps = []; alert_list = []; alert_map = []

    for item in alert_info:
        if item['severity'] == "Red" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Poor"])
        if item['severity'] == "Amber" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Moderate"])
        if item['severity'] == "Green" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Good"])

    validate_inputs(serverity_maps)
    for map_obj in serverity_maps:
        if map_obj[1] <= metric_value <= map_obj[0] :
                print(f"Threshold range for {parameter}: {map_obj}, Status : {map_obj[2]}")
                return map_obj[2]
        else:
            alert_list.append(float(map_obj[0]))
            alert_list.append(float(map_obj[1]))
            alert_map.append((float(map_obj[1]),float(map_obj[0])))

    for item in alert_info:
        if item['parameter'] == parameter and item['parameter'] in ["Accuracy", "Precision", "Recall", "F1 Score"] :
            # drift_status = "Poor" if metric_value < float(item["min_value"]) else "Good"
            drift_status = "Good" if metric_value > max(alert_list)  else "Poor" if metric_value < min(alert_list) else "Moderate"
        if item['parameter'] == parameter and not item['parameter'] in ["Accuracy", "Precision", "Recall", "F1 Score"] : 
            # drift_status = "Good" if metric_value > float(item["max_value"])  else "Poor"
            drift_status = "Poor" if metric_value > max(alert_list)  else "Good" if metric_value < min(alert_list) else "Moderate"
    
    print(f"Thresholds provided for {parameter}: {alert_map} , Status :{drift_status}")
    return drift_status

def final_recipe_status(alert_list):
    temp_info = set([st for st in alert_list if st])
    if len(temp_info)==1 and "Good" in temp_info:
        return "Good"
    elif len(temp_info) >= 1 and "Poor" in temp_info:
        return "Poor"
    else:
        return "Moderate"

def get_classification_metrics_info(reference_feature_drift_data,current_feature_drift_data,alert_info):
    drift_count = 0 
    accuracy_change = 0; precision_change = 0; recall_change = 0; f1_change = 0
    accuracy_value = current_feature_drift_data['accuracy']; precision_value = current_feature_drift_data['precision']
    re_recall_value = current_feature_drift_data['recall'] ; f1_value = current_feature_drift_data['f1']
    re_accuracy_value = reference_feature_drift_data['accuracy']; re_precision_value = reference_feature_drift_data['precision']
    recall_value = reference_feature_drift_data['recall'] ; re_f1_value = reference_feature_drift_data['f1']

    message = ''

    # Seviority Check
    accuracy_change = accuracy_value - re_accuracy_value
    accuracy_change_perc = abs(accuracy_change)/re_accuracy_value if re_accuracy_value > 0 else abs(accuracy_change)
    message += f'Accuracy has imporved by {round(accuracy_change_perc*100,2)}%, ' if accuracy_change > 0 else "No change found in Accuracy, " if accuracy_change==0 else f'Accuracy has decreased by {round(accuracy_change_perc*100,2)}%, '


    precision_change = precision_value - re_precision_value
    precision_change_perc = abs(precision_change)/re_precision_value if re_precision_value > 0 else abs(precision_change)
    message += f'Precision has imporved by {round(precision_change_perc*100,2)}%, ' if precision_change > 0 else "No change found in Precision, " if precision_change==0 else f'Precision has decreased by {round(precision_change_perc*100,2)}%, '

    recall_change = recall_value - re_recall_value
    recall_change_perc = abs(recall_change)/re_recall_value if re_recall_value > 0 else abs(recall_change)
    message += f'Recall has imporved by {round(recall_change_perc*100,2)}%, ' if recall_change > 0 else "No change found in Recall, " if recall_change==0 else f'Recall has decreased by {round(recall_change_perc*100,2)}%, '

    f1_change = f1_value -re_f1_value
    f1_change_perc = abs(f1_change)/re_f1_value if re_f1_value > 0 else abs(f1_change)
    message += f'F1 Score has imporved by {round(f1_change_perc*100,2)}%.' if f1_change > 0 else "No change found in F1 Score." if f1_change==0 else f'F1 Score has decreased by {round(f1_change_perc*100,2)}%.'

    #alert configs
    if alert_info:
        alert_configuration = get_alert_configurations("performance_drift")
        accuracy_status = check_metric_status(alert_configuration,accuracy_value,"Accuracy")
        precision_status = check_metric_status(alert_configuration,precision_value,"Precision")
        recall_status = check_metric_status(alert_configuration,recall_value,"Recall")
        f1_status = check_metric_status(alert_configuration,f1_value,"F1 Score")
    else:
        return None,message,[]

    model_performance_drift_status = final_recipe_status([accuracy_status,precision_status,recall_status,f1_status])
    plugin_name = get_plugin_name().strip().lower().replace(" ","_")

    alert_data = {
            "alert_data": {
                "recipe": plugin_name,
                "metrics": {
                    "accuracy": accuracy_value,
                    "accuracy_drift" : f"+{round(accuracy_change_perc*100,2)}%" if accuracy_change > 0 else "0%" if accuracy_change==0 else  f"-{round(accuracy_change_perc*100,2)}%",
                    "accuracy_status" : accuracy_status,

                    "precision": precision_value,
                    "precision_drift" : f"+{round(precision_change_perc*100,2)}%" if precision_change > 0 else "0%" if precision_change==0 else f"-{round(precision_change_perc*100,2)}%",
                    "precision_status" : precision_status,

                    "recall": recall_value,
                    "recall_drift" : f"+{round(recall_change_perc*100,2)}%" if recall_change > 0 else "0%" if recall_change==0 else  f"-{round(recall_change_perc*100,2)}%",
                    "recall_status" : recall_status,

                    "f1_value": f1_value,
                    "f1_score_drift" : f"+{round(f1_change_perc*100,2)}%" if f1_change > 0 else "0%" if f1_change==0  else f"-{round(f1_change_perc*100,2)}%",
                    "f1_status" :f1_status

                    },
                "status": model_performance_drift_status,
                "message": message,
                "ui_value" : model_performance_drift_status
                },
                "ai-backend-metadata": {
                "model_performance_flag": model_performance_drift_status
            }
        }
    
    alert_data = update_alert_info(alert_data)

    return model_performance_drift_status,message,alert_data

def get_regression_metrics_info(reference_feature_drift_data,current_feature_drift_data,alert_info):
    me = current_feature_drift_data["mean_error"] ; mae = current_feature_drift_data["mean_abs_error"] ; mape = current_feature_drift_data["mean_abs_perc_error"]
    re_me = reference_feature_drift_data["mean_error"] ; re_mae = reference_feature_drift_data["mean_abs_error"] ; re_mape = reference_feature_drift_data["mean_abs_perc_error"]
    message = ""

    # Seviority Check
    me_change =  me - re_me
    message += f'Mean Error(ME) has increased by {round(abs(me_change),3)}' if me_change > 0 else "No change found in Mean Error(ME), " if me_change==0 else f'Mean Error(ME) has decreased by {round(abs(me_change),3)}, '

    mae_change =  mae - re_mae
    message += f'Mean Absolute Error (MAE) has increased by {round(abs(mae_change),3)}' if mae_change > 0 else "No change found in Mean Absolute Error(MAE), " if mae_change==0 else f'Mean Absolute Error(MAE) has decreased by {round(abs(mae_change),3)}, '

    mape_change =  mape - re_mape
    message += f'Mean Absolute Percentage Error(MAPE) has increased by {round(abs(mape_change),3)}%' if mape_change > 0 else "No change found in Mean Absolute Percentage Error(MAPE), " if mape_change==0 else f'Mean Absolute Percentage Error(MAPE) has decreased by {round(abs(mape_change),3)}%, '

    #alet configs
    if alert_info:
        alert_configuration = get_alert_configurations("performance_drift")
        me_status = check_metric_status(alert_configuration,me,"ME")
        mae_status = check_metric_status(alert_configuration,mae,"MAE")
        mape_status = check_metric_status(alert_configuration,mape,"MAPE")
    else:
        return None,message,[]
    
    model_performance_drift_status = final_recipe_status([me_status,mae_status,mape_status])
    plugin_name = get_plugin_name().strip().lower().replace(" ", "_")

    alert_data = {
            "alert_data": {
                "recipe": plugin_name,
                "metrics": {
                    "ME": me,
                    "mean_error_drift" : me_change,
                    "mean_error_status" : me_status,

                    "MAE": mae,
                    "mean_absolute_error_drift" : mae_change,
                    "mean_absolute_error_status" : mae_status,

                    "MAPE": mape,
                    "mean_absolute_percentage_error_drift" : mape_change,
                    "mean_absolute_percentage_error_status" : mape_status,

                    },
                "status": model_performance_drift_status,
                "message": message,
                "ui_value" : model_performance_drift_status
                },
                "ai-backend-metadata": {
                "model_performance_flag": model_performance_drift_status
            }
        }
    
    alert_data = update_alert_info(alert_data)
    return model_performance_drift_status,message,alert_data


def get_model_metric_info(model_type,json_path):
    metrics_info = []
    model_drift_info = None ; alert_info =  None
    try:
        fh = open(json_path,"r")
        model_drift_info = json.load(fh)
        fh.close()
    except Exception as msg:
        raise Exception("Unable to read recipe.json")
    
    try:
        alert_info = json.loads(os.getenv("alert_configuration"))
    except Exception as  msg:
        raise Exception(f"not able to load alert configs : {msg}")
        

    if model_type == "classification":
        classification_metric_data = [item for item in model_drift_info["metrics"] if item["metric"]=="ClassificationQualityMetric"][0]
        current_feature_drift_data = classification_metric_data["result"]["current"]
        reference_feature_drift_data = classification_metric_data["result"]["reference"]
        return get_classification_metrics_info(reference_feature_drift_data,current_feature_drift_data,alert_info)
    
    elif model_type == "regression":
        regression_metric_data = [item for item in model_drift_info["metrics"] if item["metric"]=="RegressionQualityMetric"][0]
        current_feature_drift_data = regression_metric_data["result"]["current"]
        reference_feature_drift_data = regression_metric_data["result"]["reference"]
        return get_regression_metrics_info(reference_feature_drift_data,current_feature_drift_data,alert_info)


def get_feature_drift_report(reference:DataFrame, current:DataFrame, column_mapping=None,custom_options=None):
    color_options = get_custom_colors()
    data_drift_report = Report(metrics=[DataDriftPreset()],options=[color_options])
    data_drift_report.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
    plugin_name = get_plugin_name().strip().lower().replace(" ","_")
    html_report_path = os.path.join(os.environ["output_path"],f"{plugin_name}.html")
    json_report_path = os.path.join(os.environ["output_path"],f"{plugin_name}.json")
    # Generate the report data
    try:
        alert_info = json.loads(os.getenv("alert_configuration"))
    except Exception as  msg:
        print("Failed to load alert configurations",msg)
        data_drift_report.save_html(html_report_path)
        return html_report_path,data_drift_report
    
    if not alert_info:
        print("\nAlert configurations found empty")
        data_drift_report.save_html(html_report_path)
        return html_report_path,data_drift_report
    
    data_drift_report.save_json(json_report_path)

    try:
        fh = open(json_report_path,"r")
        feature_drift_info = json.load(fh)
        fh.close()
    except Exception as msg:
        raise Exception("Unable to read recipe.json")

    
    metrics =[metric for metric in feature_drift_info["metrics"] if metric['metric']=="DatasetDriftMetric"][0]

    acutal_feature_drift_fraction = metrics["result"]["share_of_drifted_columns"]
    actual_columns = metrics["result"]["number_of_columns"]
    drifted_columns = metrics["result"]["number_of_drifted_columns"]
    message  = f"Drift is detected for {acutal_feature_drift_fraction*100}% of columns ({drifted_columns} out of {actual_columns})."

    feature_drift_status = None
    feature_drift_alert_data = get_alert_configurations("feature_drift")
    # Seviority Check
    feature_drift_status = check_metric_status(feature_drift_alert_data,acutal_feature_drift_fraction,"Drift Score")
    feature_drift_status =  final_recipe_status([feature_drift_status])
    alert_data = {
            "alert_data": {
                "recipe": plugin_name,
                "metrics": {
                    "feature_drift": round(acutal_feature_drift_fraction,4)
                    },
                "status": feature_drift_status,
                "ui_value" : str(round(acutal_feature_drift_fraction,4)),
                "message": message
                },
                "ai-backend-metadata": {
                "feature_drift_flag": feature_drift_status
            }
        }
    
    alert_data = update_alert_info(alert_data)

    try:
        fh = open(os.getenv("output_path")+ "/alert_data.json","w")
        json.dump(alert_data,fh)
        fh.close()
    except Exception as msg:
        print("Unable to create alert_data.json")

    
        
    data_drift_report.save_html(html_report_path)
    return html_report_path,data_drift_report

def get_model_performance_drift_report(reference:DataFrame, current:DataFrame,
     problem_type=ProblemType.BINARY_CLASSIFICATION, column_mapping=None,custom_options=None,prob=False):
    color_options = get_custom_colors()
    
    plugin_name = get_plugin_name().strip().lower().replace(" ","_")
    html_report_path = os.path.join(os.environ["output_path"], f"{plugin_name}.html")
    json_report_path = os.path.join(os.environ["output_path"], f"{plugin_name}.json")

    model_status = None ; model_message = None ; alert_data = None ; drift_report = None

    if problem_type == ProblemType.BINARY_CLASSIFICATION or problem_type == ProblemType.MULTICLASS_CLASSIFICATION:
        color_options = get_custom_colors()
        if prob:
            drift_report = Report(metrics=[
                                            ClassificationQualityMetric(),
                                            ClassificationClassBalance(),
                                            ClassificationQualityByClass(),
                                            ClassificationConfusionMatrix(),
                                            ClassificationQualityByFeatureTable(),
                                            ClassificationPRCurve(),
                                            ClassificationRocCurve(),
                                            ClassificationClassSeparationPlot(),
                                            ],options=[color_options])
        else:
            drift_report = Report(metrics=[
                    ClassificationQualityMetric(),
                    ClassificationClassBalance(),
                    ClassificationQualityByClass(),
                    ClassificationConfusionMatrix(),
                    ClassificationQualityByFeatureTable(),
            ], options=[color_options])
        drift_report.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
        drift_report.save_json(json_report_path)
        try:
            alert_info = json.loads(os.getenv("alert_configuration"))
        except Exception as msg:
            print("Failed to load alert configurations", msg)
            drift_report.save_html(html_report_path)
            return html_report_path

        if not alert_info:
            print("\nAlert configurations found empty")
            drift_report.save_html(html_report_path)
            return html_report_path
        model_status,model_message,alert_data = get_model_metric_info("classification",json_report_path)
    elif problem_type == ProblemType.REGRESSION:
        color_options = get_custom_colors()
        drift_report = Report(metrics=[RegressionPreset()],options=[color_options])
        drift_report.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
        drift_report.save_json(json_report_path)
        try:
            alert_info = json.loads(os.getenv("alert_configuration"))
        except Exception as msg:
            print("Failed to load alert configurations", msg)
            drift_report.save_html(html_report_path)
            return html_report_path

        if not alert_info:
            print("\nAlert configurations found empty")
            drift_report.save_html(html_report_path)
            return html_report_path
        model_status,model_message,alert_data = get_model_metric_info("regression",json_report_path)
    else:
        print("Problem type: '"+str(problem_type) + "' not supported")

    try:
        fh = open(os.getenv("output_path")+ "/alert_data.json","w")
        json.dump(alert_data,fh)
        fh.close()
    except Exception as msg:
        print("Unable to create alert_data.json")

    drift_report.save_html(html_report_path)
    return html_report_path

def get_target_drift_report(reference:DataFrame, current:DataFrame,
     problem_type=ProblemType.BINARY_CLASSIFICATION, column_mapping=None,custom_options=None):
    # color_options = get_custom_colors()
    color_options = get_custom_colors()
    prediction_drift_dashboard = Report(metrics=[TargetDriftPreset()],options=[color_options])
    prediction_drift_dashboard.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
    plugin_name = get_plugin_name().strip().lower().replace(" ", "_")
    html_report_path = os.path.join(os.environ["output_path"], f"{plugin_name}.html")
    json_report_path = os.path.join(os.environ["output_path"], f"{plugin_name}.json")
    # Generate the report data
    try:
        alert_info = json.loads(os.getenv("alert_configuration"))
    except Exception as msg:
        print("Failed to load alert configurations", msg)
        prediction_drift_dashboard.save_html(html_report_path)
        return html_report_path, prediction_drift_dashboard

    if not alert_info:
        print("\nAlert configurations found empty")
        prediction_drift_dashboard.save_html(html_report_path)
        return html_report_path, prediction_drift_dashboard

    prediction_drift_dashboard.save_json(json_report_path)
    prediction_drift_info = None
    try:
        fh = open(json_report_path,"r")
        prediction_drift_info = json.load(fh)
        fh.close()
    except Exception as msg:
         raise Exception("Unable to read recipe.json")

    metrics = [metric for metric in prediction_drift_info['metrics'] if metric["metric"]=="ColumnDriftMetric"][0]
    prediction_score = metrics["result"]["drift_score"]
    drift_detected = metrics["result"]["drift_detected"]
    detection_method = metrics["result"]["stattest_name"]
    message = f"Drift detected. Drift detection method: {detection_method}. Drift score: {prediction_score}" if drift_detected else f"Data drift not detected. Drift detection method: {detection_method}. Drift score: {prediction_score}"
    prediction_drift_alert_data = get_alert_configurations("prediction_drift")
    prediction_drift_status = check_metric_status(prediction_drift_alert_data,prediction_score,"Drift Score")

    prediction_drift_status = final_recipe_status([prediction_drift_status])

    alert_data = {
            "alert_data": {
                "recipe": plugin_name,
                "metrics": {
                    "score": prediction_score
                    },
                "status": prediction_drift_status,
                "message": message,
                "ui_value" : prediction_drift_status,
                },
                "ai-backend-metadata": {
                "prediction_drift_flag": prediction_drift_status
            }
        }
    
    alert_data = update_alert_info(alert_data)
    try:
        file_path = os.path.join(os.getenv("output_path"),"alert_data.json")
        fh = open(file_path,"w")
        json.dump(alert_data,fh)
        fh.close()
    except Exception as msg:
        print("Unable to create alert_data.json",msg)

    prediction_drift_dashboard.save_html(html_report_path)
    return html_report_path
