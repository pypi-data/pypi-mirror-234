import imp
# from typing import Tuple
from utility.connector.connector import Connector
from pandas import DataFrame, read_csv
from refractio.refractio import get_local_dataframe

class Refract(Connector):
    def __init__(self, dataset):
        self.dataset = dataset

    def load_data(self) -> DataFrame:
        dataset_path = f"/data/{self.dataset}"
        try:
            dataset = get_local_dataframe(dataset_path)
            return dataset
        except:
            print("Error while loading the data from filesystem. Path enrered -"+ dataset_path )
            return None