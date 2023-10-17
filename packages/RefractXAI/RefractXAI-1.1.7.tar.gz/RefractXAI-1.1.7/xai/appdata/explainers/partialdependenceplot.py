from .base import ModelInterpreter
from skater.core.explanations import Interpretation
from skater.model import InMemoryModel
from tqdm.auto import tqdm
from ..constants import Log
from ..logging import build_logger

logger = build_logger(Log.logger_level, "pdp")


class PartialDependencePlot(ModelInterpreter):
    """
        This class is used to generate partial dependence plots for a model.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: A partial dependence plot object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)
        # initialize the super class

        self.target_pdp_names = self.target_names
        if not self.mode == "regression":
            self.target_names = self.unique_values

        # initialize the interpreter
        self.interpreter = Interpretation(
            training_data=self.x_test,
            # training_labels=self.y_train,
            feature_names=self.feature_names,
            # class_names=self.unique_values,
        )

        # initialize the in memory model
        if not self.mode == "regression":
            self.in_memory_model = InMemoryModel(
                prediction_fn=self.model.predict_proba,
                examples=self.x_train,
                target_names=self.target_names,
            )
        else:
            self.in_memory_model = InMemoryModel(
                prediction_fn=self.model.predict,
                examples=self.x_train,
                target_names=self.target_names,
                feature_names=self.feature_names,
                model_type="regressor"
            )

    def generate_data(self):
        """
            Generates the data for the partial dependence for the feature ids provided

            Returns:
                list: A list of json values for partial dependence plots.

        """

        dict_list = []
        binaryMode = 'true'

        if len(self.target_names) >2 :
            binaryMode = 'false'


        if self.mode == "multiclassification" or self.mode == "binaryclassification":
            for feat in tqdm(self.feature_ids):
                axes_list = self.interpreter.partial_dependence.partial_dependence(
                    [feat],
                    self.in_memory_model,
                    n_jobs=1
                )
                yax = {}
                
                temp_target_names = []
                for j in range(len(self.target_names)):
                    if j in axes_list.columns:
                        temp = {self.process_obj['labelInfo'][f'{self.target_names[j]}']: axes_list[self.target_names[j]].tolist()}
                        temp_target_names.append(self.process_obj['labelInfo'][f'{self.target_names[j]}'])
                        yax.update(temp)
                        
                dict_list.append({
                    "feature_name" : feat,
                    "feature_data" : list(axes_list[feat].to_numpy()),
                    "pdp_values" : yax,
                    "binaryMode": binaryMode
                })

            return dict_list,temp_target_names,self.mode
        if self.mode == "regression":
            for feat in tqdm(self.feature_ids):
                axes_list = self.interpreter.partial_dependence.partial_dependence(
                    [feat],
                    self.in_memory_model,
                    n_jobs=1
                )

                target_name = self.target_pdp_names[0]
                dict_list.append({
                    "feature_name" : feat,
                    "feature_data" : list(axes_list[feat].to_numpy()),
                    "pdp_values" : axes_list[target_name].tolist(),
                    "regressionMode": "true"
                })

            return dict_list, self.target_names,self.mode

        return dict_list,"nlg"