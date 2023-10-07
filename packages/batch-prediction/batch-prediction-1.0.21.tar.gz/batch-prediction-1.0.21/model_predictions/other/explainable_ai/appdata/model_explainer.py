# -*- coding: utf-8 -*-
from .utils import find_unique_values, generate_predict_fn, generate_sample_request
from .explainers.partialdependenceplot import PartialDependencePlot
from .explainers.featureimportance import FeatureImportance
from .explainers.limeforceplot import LimeForcePlot
from .explainers.decisionplot import DecisionPlot
from .explainers.overview import ModelOverView

from .constants import Log
from .logging import build_logger



class ModelExplainer:
    """
            Class to create Model Explainer base object for Explainable Ai

            Args:
                model : Model Object
                x_train : Training data Feature Values
                y_train : Training data Target Values
                feature_names : Names of Columns
                feature_ids : Selective Names of Columns for the Graphs
                target_names : Target Column Names
                preprocessing : Function to handle preprocessing operations,
                sample_req : Sample request object to be sent for scoring,

            Returns:
                object: ModelExplainer Object

            Examples
            --------
            from refractexplainer.model_explainer import ModelExplainer
            me = ModelExplainer(model=clf, x_train=X, y_train=y, feature_names=fn, feature_ids=fn)
            me.partial_dependence.generate_image()
            me.partial_dependence.generate_data()
    """

    def __init__(
            self,
            model,
            x_train,
            y_train,
            x_test,
            y_test,
            sample_rows,
            feature_names,
            target_names,
            process_obj,
            mode=None,
            feature_ids=None,
            preprocessing=None,
            sample_req=None,
            predict_fn=None
    ):
        self.x_test = x_test
        self.process_obj = process_obj
        self.model = model
        self.y_test = y_test
        self.x_train = x_train
        self.y_train = y_train
        self.feature_names = feature_names
        self.target_names = target_names
        self.sample_rows = sample_rows
        self.feature_ids = feature_ids if feature_ids else feature_names
        self.mode = mode if mode else 'classification'
        self.preprocessing = preprocessing
        self.sample_req = sample_req if sample_req else generate_sample_request(x_train)

        self.unique_values = find_unique_values(self.y_train)

        self.predict_fn = predict_fn if predict_fn else generate_predict_fn(self.model, self.mode, self.preprocessing)

        # print("Inside Model_explainer.py  - 1")
        self.ml_overview = ModelOverView(self)
        self.fi = FeatureImportance(self)
        self.lf = LimeForcePlot(self)
        self.pdp = PartialDependencePlot(self)
        self.dplot = DecisionPlot(self)


    





