import imp
from typing import Tuple
from utility.connector.connector import Connector
from pandas import DataFrame, read_csv
from refractio.refractio import get_local_dataframe

class Refract(Connector):
    def __init__(self, reference_data, current_data):
        self.reference_data_path = f"/data/{reference_data}"
        self.current_data_path = f"/data/{current_data}"

    def load_data(self) -> Tuple[DataFrame, DataFrame]:
        try:
            referance_table = get_local_dataframe(self.reference_data_path)
            current_table = get_local_dataframe(self.current_data_path)
            return referance_table, current_table
        except Exception as msg:
            print(msg)
            print("Error while loading the data from filesystem. Path enrered - current: '"+self.current_data_path
            +"' and reference - '"+self.reference_data_path+"'")
            return None