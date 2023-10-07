import json
from .base import ModelInterpreter
from ..constants import Log
import shap
import warnings
import numpy as np
from ..logging import build_logger

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score ,roc_auc_score,log_loss

class ModelOverView(ModelInterpreter):
    """
        This class is used to explain the model using lime.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: The lime explainer object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.unique_values = tuple(map(lambda num: int(float(num)), tuple(self.unique_values)))


    def generate_data(self):
        from sklearn.metrics import f1_score,precision_score,recall_score,confusion_matrix,accuracy_score
        metric_payload = {}
        predicted = self.model.predict(self.x_test)
        model_type = self.mode

        if model_type == "multiclassification":
            ## Confusion Matrix
            metric_payload["confusion_matrix_ui"] = confusion_matrix(predicted,self.y_test)

            ## Metrcis Info
            ml_data = {
                "Accuracy Score ": accuracy_score(predicted,self.y_test),
                "F1 Score": f1_score(predicted,self.y_test, average="micro"),
                "Recall Score": recall_score(predicted,self.y_test, average="weighted"),
                "Precision Score": precision_score(predicted,self.y_test, average='macro')
            }
            metric_payload["metrics"] = ml_data
            ## ROC-AUC Curve
            import sklearn.metrics as metrics
            probs = self.model.predict_proba(self.x_test)
            temp_payload = {}
            no_classes = probs.shape[1]
            for i in range(no_classes):
                fpr, tpr, threshold = metrics.roc_curve(self.y_test, probs[:,i], pos_label=i)
                print(fpr)
                roc_auc = metrics.auc(fpr, tpr)
                data = [[x, y] for x, y in zip(list(fpr), list(tpr))]
                maxValue = max(list(tpr))
                temp_payload[self.process_obj["labelInfo"][f"{i}"]] = {
                    "payload" :data,
                    "auc_score": roc_auc,
                    "maxValue": maxValue
                }

            metric_payload["roc_auc"] = temp_payload

            json_confusion_matrix = []
            for ele in list(metric_payload["confusion_matrix_ui"]):
                json_confusion_matrix.append(ele.tolist())

            metric_payload["confusion_matrix"]=json_confusion_matrix


            # roc_auc
        if model_type == "binaryclassification":
            metric_payload["confusion_matrix_ui"] = confusion_matrix(self.y_test,predicted)

            ml_data = {
                "Accuracy Score ": accuracy_score(predicted,self.y_test),
                "F1 Score": f1_score(predicted,self.y_test),
                "Recall Score": recall_score(predicted,self.y_test),
                "Precision Score": precision_score(predicted,self.y_test)
            }
            metric_payload["metrics"] = ml_data
            ## ROC-AUC Curve
            import sklearn.metrics as metrics
            probs = self.model.predict_proba(self.x_test)
            temp_payload = {}
            no_classes = probs.shape[1]
            for i in range(no_classes):
                fpr, tpr, threshold = metrics.roc_curve(self.y_test, probs[:,i], pos_label=i)
                roc_auc = metrics.auc(fpr, tpr)
                data = [[x, y] for x, y in zip(list(fpr), list(tpr))]
                maxValue = max(list(tpr))
                temp_payload[self.process_obj["labelInfo"][f"{i}"]] = {
                    "payload" :data,
                    "auc_score": roc_auc,
                    "maxValue": maxValue
                }
            metric_payload["roc_auc"] = temp_payload

            json_confusion_matrix = []
            for ele in list(metric_payload["confusion_matrix_ui"]):
                json_confusion_matrix.append(ele.tolist())

            metric_payload["confusion_matrix"]=json_confusion_matrix

        if model_type == "regression":
            from sklearn.metrics import (
                mean_absolute_error,
                mean_squared_error,
                r2_score,
                adjusted_rand_score
            )
            y_test = self.y_test
            y_pred = self.model.predict(self.x_test)

            ######## Metrics
            ml_data = {
                "Mean Absolute Error" : mean_absolute_error(y_pred, y_test),
                "Mean Squared Error" : mean_squared_error(y_pred, y_test),
                "R2 Score" : r2_score(y_pred, y_test),
                "Adjusted Rand score " : adjusted_rand_score(y_pred.ravel(), y_test.ravel()),
                
            }
            metric_payload["metrics"]=ml_data
            ## Regression Plot
            temp = {}
            temp["rangePayload"] = {
                "x_min":min(y_test.ravel()),
                "x_max":max(y_test.ravel()),
                "y_max":max(y_pred.ravel()),
                "y_min":min(y_pred.ravel())
            }
            temp["regData"]=[[x,y] for x,y in zip(y_test.ravel(),y_pred.ravel())]
            temp["target_name" ] = self.target_names[0]

            metric_payload["regression_plot"] = temp
        return  metric_payload

    def validate_sample_req(self):
        """
            Validates the sample request.

        """
        import numpy as np
        self.sample_req = np.array(self.sample_req)
        if isinstance(self.sample_req, np.ndarray) and self.sample_req.shape[0] == len(self.feature_names):
            # print("Pass")
            pass
        else:
            raise ValueError("Sample request should be a numpy array for single row eg. np.array([1,2,3])")
