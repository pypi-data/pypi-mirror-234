import json
from .base import ModelInterpreter
from ..constants import Log
import shap
import warnings
import numpy as np
from ..logging import build_logger

class DecisionPlot(ModelInterpreter):
    """
        This class is used to explain the model using lime.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: The lime explainer object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)
        # initialize the super class
        self.unique_values = tuple(map(lambda num: int(num), tuple(self.unique_values)))

    def generate_data(self,fi_explainer,shap_values):
        shap_data = {}
        sample_rows = self.sample_rows

        if self.mode == "multiclassification" or self.mode == "binaryclassification":
            # explainer = shap.Explainer(self.model)
            # explainer = shap.KernelExplainer(self.model.predict_proba,self.x_test)
            # expected_values = explainer.expected_value.tolist()
            # shap_values  = explainer.shap_values(self.x_test)
            expected_values = fi_explainer.expected_value.tolist()
            tempClassInfo = {}
            for classValue in range(len(shap_values)):
                tempRowInfo = {}
                expectedValue = expected_values[classValue]
                classShaps = shap_values[classValue]
                sortedIndexes = np.argsort(np.sum(np.abs(classShaps),axis=0)).tolist()
                classShapsSorted = classShaps[:,sortedIndexes] + expectedValue
                features_display = [self.feature_names[i] for i in sortedIndexes]
                for row_no in sample_rows:
                    temp = {}
                    # row_data = classShaps[row_no]
                    dplotData = classShapsSorted[row_no].tolist()
                    temp["data"] = dplotData
                    temp["min"] =  min(dplotData)
                    temp["max"] = max(dplotData)
                    temp["meanValue"] = expectedValue
                    temp["features_display"] = features_display
                    temp["start_y"] = features_display[0]
                    temp["end_y"] = features_display[-1]
                    temp['target_name'] = "Model Prediction Probabilities"
                    tempRowInfo[row_no]=temp

                # tempClassInfo[f"class_{classValue}"]=tempRowInfo
                tempClassInfo[self.process_obj["labelInfo"][f"{classValue}"]] = tempRowInfo

            shap_data["classificationDplot"]=tempClassInfo
            shap_data["modelInfo"]={"name": "classification", "no_classes": len(expected_values)}
            
        if self.mode == "regression":
            # explainer = shap.Explainer(self.model)
            explainer = shap.KernelExplainer(self.model.predict,self.x_test)
            shap_values = explainer.shap_values(self.x_test)
            expected_value = explainer.expected_value
            shap_values = shap_values + expected_value
            features_display = self.feature_names
            tempRowInfo = {}
            for row_no in sample_rows:
                temp = {}
                row_shaps = shap_values[row_no].tolist()
                dplotData = [round(x,3) for x in row_shaps]
                temp["data"] = dplotData
                temp["min"] = min(dplotData)
                temp["max"] = max(dplotData)
                temp["meanValue"] = expected_value
                temp["features_display"] = features_display
                temp["start_y"] = features_display[0]
                temp["end_y"] = features_display[-1]
                temp['target_name'] = self.target_names[0]
                tempRowInfo[row_no] = temp
            shap_data["regressionDplot"] = tempRowInfo

        return shap_data

    def validate_sample_req(self):
        """
            Validates the sample request.

        """
        import numpy as np
        self.sample_req = np.array(self.sample_req)
        if isinstance(self.sample_req, np.ndarray) and self.sample_req.shape[0] == len(self.feature_names):
            # print("Pass")
            pass
        else:
            raise ValueError("Sample request should be a numpy array for single row eg. np.array([1,2,3])")
