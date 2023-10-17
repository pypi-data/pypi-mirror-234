
import pandas as pd
from .artifacts import get_loader
from pandas import DataFrame,Series
import os,tarfile
from constants import ModelConstants
from os import path
import json,subprocess
import numpy as np
from bs4 import BeautifulSoup as Soup
import importlib.util as imu
from .get_user_data import Userdata

def pickle_loads(file_path):
    from os import path
    if os.stat(file_path).st_size <=5:
        raise Exception(f"{file_path} file data is too small, less than 5 bytes")
    
    if path.exists(file_path):
        pickled_file = open(file_path, "rb")
        obj = pd.compat.pickle_compat.load(pickled_file)
        pickled_file.close()
        return obj


class ModelArtifacts:
    def __init__(self,model_path) -> None:
        self.model_path = model_path
        self.labels = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.meta_info = None
        self.model_file_path = None

    def download_model_artifacts(self):
        model_file_name = "ml_model.tar.gz"
        tar = tarfile.open(os.path.join(self.model_path,model_file_name))
        tar.extractall(path=ModelConstants.MODEL_DIR)
        tar.close()

        # self.meta_info = pickle_loads(os.path.join(ModelConstants.MODEL_DIR, ModelConstants.Meta_Info))
        self.x_train = pickle_loads(os.path.join(ModelConstants.MODEL_DIR, ModelConstants.X_TRAIN))
        self.y_train = pickle_loads(os.path.join(ModelConstants.MODEL_DIR, ModelConstants.Y_TRAIN))
        self.model_file_path = os.path.join(ModelConstants.MODEL_DIR, ModelConstants.MODEL_FILE)
        
        # self.x_test = pickle_loads(os.path.join(ModelConstants.MODEL_DIR, ModelConstants.X_TEST))
        # self.y_test = pickle_loads(os.path.join(ModelConstants.MODEL_DIR, ModelConstants.Y_TEST))
        # features_name = self.meta_info["model_info"]["features_name"]
        # target_names = self.meta_info["model_info"]["targets_mapping"]["target_names"]

        user_data = Userdata()
        self.x_test = user_data.test_table
        self.y_test = user_data.test_target
        feature_names  = user_data.feature_names
        target_names = [user_data.target_name]
    
        return {
            'x_train' : self.x_train,
            'x_test' : self.x_test,
            'y_train' : self.y_train,
            'y_test' : self.y_test,
            'feature_names' : feature_names,
            'target_names' : target_names
        }

    
    def pickle_load_label_map(self,model_type):
        file_path = os.path.join(ModelConstants.MODEL_DIR, ModelConstants.Reverse_Map)
        if path.exists(file_path):
            pickled_file = open(file_path, "rb")
            obj = pickle_loads(pickled_file)
            return obj
        else:
            if not model_type == "regression":
                unique_values = self.get_unique_values()
                label_info = {str(i):str(i) for i in unique_values}
                out_data = {
                        "labelInfo" :label_info,
                        "featureInfo" : {}
                    }
                return out_data
            else:
                return {
                        "labelInfo" :{},
                        "featureInfo" : {}
                    }

    def get_unique_values(self):
        testArray = self.y_test
        if isinstance(testArray,pd.core.frame.DataFrame):
            testArray = testArray.to_numpy()
        if isinstance(testArray, np.ndarray):
            unique_values = np.unique(testArray).tolist()
        elif isinstance(testArray, pd.core.series.Series):
            unique_values = testArray.unique().tolist()
        else:
            raise Exception("Array Entered is neither Pandas Series df nor numpy array")
        self.labels = unique_values
        return self.labels
    

    def get_column_names(self,data):
        if isinstance(data,DataFrame):
            return data.columns.tolist()
        elif isinstance(data,Series):
            return data.to_frame().columns.tolist()
        return []

    
    def load_model(self,flavour):
        try:
            loader = get_loader(flavour)
            return loader(self.model_file_path)
        except Exception as msg:
            raise Exception("Model loading is failed",msg)
    
    def install_model_dependencies(self):
        try:
            requirments = os.path.join(ModelConstants.MODEL_DIR, ModelConstants.Requirments)
            if not path.exists(requirments):
                print("model requirments.txt file not found")
                return None
            self.requirements = pickle_loads(requirments)
            packages= self.requirements["pip_packages"]
            for package in packages.split():
                package_name = package.split("==")
                if package_name and not imu.find_spec(package_name):
                    subprocess.check_call(["python","-m","pip","install",package])
            
            print("Model dependencies are installed")

        except Exception as msg:
            print(msg)
            raise Exception("Failed to install model dependencies")


    def get_model_artifacts(self) -> dict:
        data = self.download_model_artifacts()

        return data

class XAIHTML:
    def __init__(self,output_path,target_class_names=None) -> None:
        self.html_path = os.path.join(os.getcwd(),"template.html")
        self.output_path = output_path
        self.soup = Soup(open(self.html_path), "html.parser")
        self.target_class_names = target_class_names


    def load_html(self,**params):
        soup = self.soup
        all_scripts = soup.find_all('script')

        for div in  soup.find_all("div"):
            if div.get("id")=="multi_classlabels":
                    div.clear()
                    if "multi_class_labels" in params and params["multi_class_labels"]:
                        div.insert(1, params["multi_class_labels"])
            if div.get("id") == "multi_classlabels_roc":
                    div.clear()
                    if "multi_class_labelsroc" in params and params["multi_class_labelsroc"]:
                        div.insert(1, params["multi_class_labelsroc"])
            if div.get("id") == "lime_row_class_list":
                    div.clear()
                    if "insert_multi_class_labels_lime" in params and  params["insert_multi_class_labels_lime"]:
                        div.insert(1, params["insert_multi_class_labels_lime"])
            if div.get("id")=="lime_row_dropdown_list":
                div.clear()
                if "insert_random_rows_lime" in params:
                    div.insert(1,params["insert_random_rows_lime"])
            if div.get("id")=="pdp_dropdown_list":
                div.clear()
                if "pdp_features_names" in params:
                    div.insert(1,params["pdp_features_names"])
            if div.get("id")=="pdp_class_list":
                div.clear()
                if "htmlClassLabelsPDP" in params and  params["htmlClassLabelsPDP"]:
                    div.insert(1,params["htmlClassLabelsPDP"])
            if div.get("id")=="list_dplot_rows_content":
                div.clear()
                if "insert_dplot_rows" in params:
                    div.insert(1,params["insert_dplot_rows"])
            if div.get("id")=="list_dplot_classes":
                div.clear()
                if "insert_dplot_classes" in params and params["insert_dplot_classes"]:
                    div.insert(1,params["insert_dplot_classes"])
        
        ########## Script Tags ################
        for text in all_scripts:
            if text.get("id") == "modelstats_overview_script" :
                text.clear()
                if "model_overview_html_script" in params:
                    text.insert(1,params["model_overview_html_script"])
            if text.get("id") == "featureimportance_script" :
                text.clear()
                if "feature_importance" in params:
                    text.insert(1,params["feature_importance"])
            if text.get("id") == "lime_plot_data_script":
                text.clear()
                if "lime_plot_data" in params:
                    text.insert(1,params["lime_plot_data"])
            if text.get("id") == "script_pdp_plots" :
                text.clear()
                if "pdp_plot_data" in params:
                    text.insert(1,params["pdp_plot_data"])
            if text.get("id") == "script_dplot_plots":
                text.clear()
                if "dplot_explainer_html" in params:
                    text.insert(1,params["dplot_explainer_html"])

        ########### Added Classnames for classificatoin Problems ##################
        self.add_class_names()

        ## Dump html
        self.write_html()

    def read_html(self):
        try:
            fh = open("xai.html","r")
            html_content = fh.read()
            fh.close()
        except Exception as msg:
            raise Exception(msg)

        print("Reading HTML")
        return html_content

    def custom_prettify(self):
        soup = self.soup
        """Custom function to format prettified BeautifulSoup output."""
        return soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ')
                                        .replace('<', '\n<')
                                        .replace('>', '>\n')
                                        .replace('\n\n', '\n')
                                        .replace('\n', os.linesep))

    def write_html(self):
        try:
            file_loc = os.path.join(self.output_path,"model_explanations.html")
            fh = open(file_loc,"w",encoding='utf-8')
            output_data = self.custom_prettify()
            # print(output_data)
            fh.write(output_data)
            fh.close()
        except Exception as msg:
            print(msg)
            print("Unable to save XAI HTML " )
        
        print("XAI Completed")
    
    def save_json_file(self,**params_info):
        try:
            # print(dict(params_info))
            file_loc = os.path.join(self.output_path,"explainableAi.json")
            fh = open(file_loc,"w")
            json.dump(dict(params_info), fh)
            fh.close()
        except Exception as msg:
            print(msg)
            print("Unable to save XAI JSON  " )
    
    def add_class_by_select_id(self,select_id):
        select_element = self.soup.fin("select",{"id":select_id})
        for option in select_element.find_all('option'):
            value = option.text
            if value in self.target_class_names:
                option["value"] = value
                option.string = self.target_class_names[value]

    def add_class_names(self):
        for select_id in ["multi_classlabels","multi_classlabels_roc","pdp_class_name","dplot_class_name","list_lime_class"]:
            self.add_class_by_select_id(select_id)


