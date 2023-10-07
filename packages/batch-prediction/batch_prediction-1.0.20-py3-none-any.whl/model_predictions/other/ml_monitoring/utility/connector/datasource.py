from typing import Tuple
from pandas import DataFrame
from refractio.refractio import get_dataframe
import os
from utility.connector.connector import Connector


class RefractIO(Connector):
    def __init__(self, ref_table, current_table) -> None:
        self.ref_table = ref_table
        self.current_table = current_table
        
    def load_data(self) -> Tuple[DataFrame, DataFrame]:
        try:
            project_id = os.getenv("PROJECT_ID")
            max_row_count = self._get_configs()['max_row_count']
            print(f"Reading reference dataframe: {self.ref_table} using,\n"
                  f"project_id: {project_id}\n"
                  f"row_count: {max_row_count}\n"
                  f"filter_condition: {os.getenv('reference_filter_condition')}")
            referance_table = get_dataframe(self.ref_table,
                                            project_id=project_id,
                                            row_count=max_row_count,
                                            filter_condition=os.getenv("reference_filter_condition"))
            print(f"reference dataframe read using refractio,\n"
                  f"referance_table.head(3):\n{referance_table.head(3)}\n"
                  f"referance_table.shape: {referance_table.shape}")
            print(f"Reading current dataframe: {self.current_table} using,\n"
                  f"filter_condition: {os.getenv('current_filter_condition')}")
            current_table = get_dataframe(self.current_table,
                                          project_id=project_id,
                                          row_count=max_row_count,
                                          filter_condition=os.getenv("current_filter_condition"))
            print(f"current dataframe read using refractio,\n"
                  f"current_table.head(3):\n{current_table.head(3)}\n"
                  f"current_table.shape: {current_table.shape}")
            return referance_table, current_table

        except Exception as msg:
            print(msg)
            print("Error while loading the data from RefractIO.")
            return None

    def _get_configs(self):
        import configparser
        parser = configparser.ConfigParser()
        parser.read('utility/properties.ini')
        max_row_count=int(parser['constants']['max_row_count'])
        return {'max_row_count':max_row_count}
