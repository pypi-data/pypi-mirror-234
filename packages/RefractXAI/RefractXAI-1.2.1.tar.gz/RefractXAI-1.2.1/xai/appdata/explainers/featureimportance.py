import json
from .base import ModelInterpreter
from skater.core.explanations import Interpretation
from skater.model import InMemoryModel
from ..constants import Log
import numpy as np
import shap
from ..logging import build_logger

logger = build_logger(Log.logger_level, "fi")


class FeatureImportance(ModelInterpreter):
    """
        This class is used to generate feature importance for a model.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: The feature importance object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)

        if self.mode == "classification":
            self.target_names = self.unique_values
        
        self.fi_explainer = None
        self.shap_values = None



    def generate_data(self):
        """
            Generates the data for the feature importance.

            Returns:
                list: A list of dictionaries containing the feature importance data.

        """

        model_type = self.mode

        if model_type in ["multiclassification","binaryclassification"]:
            # explainer = shap.Explainer(self.model)
            # explainer = shap.KernelExplainer(self.model.predict_proba,self.x_test)
            self.fi_explainer = shap.KernelExplainer(self.model.predict_proba,self.x_test)
            self.shap_values = self.fi_explainer.shap_values(self.x_test)
            shap_values= self.shap_values
            dictWeights = {}
            for i in range(len(shap_values)):
                instanceShaps = shap_values[i]
                #sorting weights
                sortedIdx = np.argsort(np.sum(np.abs(instanceShaps),axis=0))
                sortedShaps = instanceShaps[:,sortedIdx]

                sortedFeatureNames = np.array(self.feature_names)[sortedIdx].tolist()
                sortedWeights = np.sum(np.abs(sortedShaps),axis=0).tolist()
                sortedWeights = self.generated_fi_percentages(sortedWeights)
                sortedWeights = [round(x,3) for x in sortedWeights]
                className = self.process_obj["labelInfo"][f"{i}"]
                dictWeights[className] = dict(zip(sortedFeatureNames,sortedWeights))
            dictWeights["model_target_info"] = {"target_name" : self.target_names[0]}
                
            
            return dictWeights


        if model_type == "regression" :
            self.interpreter = Interpretation(
                training_data=self.x_train,
                feature_names=self.feature_names,
            )

            self.in_memory_model = InMemoryModel(
                prediction_fn=self.model.predict,
                examples=self.x_train,
                target_names=self.target_names,
                feature_names=self.feature_names,
                model_type="regressor"
            )
            fi = self.interpreter.feature_importance.feature_importance(
                model_instance=self.in_memory_model,
                ascending=False,
            )
            dataWeights = dict(fi)
            sortedWeights = {k: round(v*100,3) for k, v in sorted(dataWeights.items(), key=lambda item: item[1])}
            # nm_data = sortedWeights
            print(sortedWeights)

            return {
                "model_target_info" :{"target_name" : self.target_names[0]},
                "predictions":sortedWeights
            }
        
    def generated_fi_percentages(self,data):
        maximum = sum(data)
        updated_values = [(x/maximum)*100 for x in data]
        return updated_values
