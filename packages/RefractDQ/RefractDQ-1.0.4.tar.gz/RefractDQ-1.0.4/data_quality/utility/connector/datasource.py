from pandas import DataFrame
from utility.connector.connector import Connector
from refractio.refractio import get_dataframe
import os


class RefractIO(Connector):
    def __init__(self,dataset) -> None:
        self.dataset=dataset
        
    def load_data(self) -> DataFrame:
        try:
            project_id = os.getenv("PROJECT_ID")
            max_row_count = self._get_configs()['max_row_count']
            print(f"Reading refract dataset {self.dataset} using,\n"
                  f"project_id: {project_id}\n"
                  f"row_count: {max_row_count}\n"
                  f"filter_condition: {os.getenv('filter_condition')}")
            dataset = get_dataframe(self.dataset,
                                    project_id=project_id,
                                    row_count=max_row_count,
                                    filter_condition=os.getenv("filter_condition")
                                    )
            print(f"dataset read using refractio,\n"
                  f"dataset.head(3):\n{dataset.head(3)}\n"
                  f"dataset.shape: {dataset.shape}")
            return dataset

        except Exception as msg:
            print(msg)
            print("Error while loading the data from Refract IO.")
            return None
        
    def _get_configs(self):
        import configparser
        parser = configparser.ConfigParser()
        parser.read('utility/properties.ini')
        max_row_count=int(parser['constants']['max_row_count'])

        return {'max_row_count':max_row_count}

