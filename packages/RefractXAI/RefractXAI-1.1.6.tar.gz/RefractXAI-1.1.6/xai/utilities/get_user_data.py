
from refractio.refractio import get_local_dataframe
from refractio.refractio import get_dataframe
import pandas as pd
import os,json 

class Userdata:
    def __init__(self) -> None:
        self.test_table = None
        self.test_target = None
        self.feature_names = []
        self.target_name = []
        self.datasource = None
        self.dataset_name = None
        self.get_data()
    
    def get_data(self):
        dataframe = None
        self.datasource = os.getenv("data_source")
        self.dataset_name = os.getenv("current_data_path")
        if self.datasource == "Local data files":
            dataframe = get_local_dataframe(f"/data/{self.dataset_name}")
        if self.datasource == "refract datasets":
            dataframe = get_dataframe(self.dataset_name)
            
        return self.get_info(dataframe)
    
    def get_info(self,dataframe):
        self.get_target_name()
        self.test_target = dataframe[self.target_name]
        self.test_table = dataframe.drop(columns=[self.target_name])
        self.feature_names = list(self.test_table.columns)

    def get_target_name(self):   
        basic_details = json.loads(os.getenv("current_dataset"))
        self.target_name = [item["field_value"] for item in basic_details if item["field_id"]=="target_column"][0]