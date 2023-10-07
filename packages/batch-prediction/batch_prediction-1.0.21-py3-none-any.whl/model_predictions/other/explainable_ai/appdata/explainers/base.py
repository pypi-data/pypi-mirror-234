"""Base ModelInterpreter class. submodules like lime and partial dependence"
must have these methods"""
from ..logging import build_logger
from ..constants import Log

logger = build_logger(Log.logger_level, "fi")


class ModelInterpreter(object):
    """
    Base Interpreter class. Common methods include loading a dataset and type setting.
    """

    def __init__(self, interpreter):
        self.x_test = interpreter.x_test
        self.y_test = interpreter.y_test
        self.model = interpreter.model
        self.x_train = interpreter.x_train
        self.y_train = interpreter.y_train
        self.feature_names = interpreter.feature_names
        self.sample_rows = interpreter.sample_rows
        self.target_names = interpreter.target_names
        self.process_obj = interpreter.process_obj
        self.feature_ids = interpreter.feature_ids
        self.mode = interpreter.mode
        self.preprocessing = interpreter.preprocessing
        self.sample_req = interpreter.sample_req
        self.unique_values = interpreter.unique_values
        self.predict_fn = interpreter.predict_fn

    def generate_data(self):
        pass

    def generate_image(self):
        pass

    def generate_local_explaination(self):
        pass
