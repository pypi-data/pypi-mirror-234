import os,json
from utility.connector.connector import Connector
from utility.connector.refract import Refract
from utility.connector.datasource import RefractIO

from utility import constants 

def get_dataset_names():
        try:
            refract_refer_dataset = json.loads(os.getenv("reference_dataset"))
            refract_cur_dataset = json.loads(os.getenv("current_dataset"))
            reference_data = [item["field_value"] for item in refract_refer_dataset if item["field_id"]=="reference_data_path"][0]
            current_data = [item["field_value"] for item in refract_cur_dataset if item["field_id"]=="current_data_path"][0]
            return reference_data,current_data
        except Exception as msg:
            print(msg)
            print(f"Unable to load datasets details from ENV: error - {msg} ")

class ConnectorFactory:
    
    def getConnector(connector) -> Connector:
        if connector.lower() == constants.DataConnector.REFRACT_DATASETS :
            print("Fetching datasets from RefractIO")
            ref_dataset,cur_dataset = get_dataset_names()
            connection = RefractIO(ref_dataset,cur_dataset)

            return  connection
        elif connector.lower() == constants.DataConnector.REFRACT_LOCAL_FILES:
            ref_dataset,cur_dataset = get_dataset_names()
            connection = Refract(ref_dataset,cur_dataset)
            return connection
        else:
            print("Source Not Supported! User provided : {}, expected one from [{},{}]".format(connector,constants.DataConnector.SNOWFLAKE,constants.DataConnector.REFRACT_FILE))
            return None
    
