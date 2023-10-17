import os,json
from utility.connector.connector import Connector
from utility.connector.refract import Refract
from utility.connector.datasource import RefractIO

from utility import constants 

class ConnectorFactory:
    def getConnector(connector) -> Connector:
        if connector.lower() == constants.DataConnector.REFRACT_DATASETS :
            try:
                refract_refer_dataset = json.loads(os.getenv("reference_dataset"))
                data_set = [item["field_value"] for item in refract_refer_dataset if item["field_id"]=="reference_data_path"][0]
            except Exception as msg:
                print(msg)
                raise Exception(f"Unable to load datasets details from ENV ")
            
            connection = RefractIO(data_set)

            return  connection
        elif connector.lower() == constants.DataConnector.REFRACT_LOCAL_FILES:
            print(f"Fetching data from ${connector}")
            try:
                refract_refer_dataset = json.loads(os.getenv("reference_dataset"))
                data_set = [item["field_value"] for item in refract_refer_dataset if item["field_id"]=="reference_data_path"][0]
            except Exception as msg:
                print(msg)
                raise Exception(f"Unable to load datasets details from ENV ")
            
            connection = Refract(data_set)
            
            return connection
        else:
            print(f"Source Not Supported! User provided : {connector}, expected one from [f{constants.DataConnector.REFRACT_DATASETS},f{constants.DataConnector.REFRACT_LOCAL_FILES}]")
            return None
