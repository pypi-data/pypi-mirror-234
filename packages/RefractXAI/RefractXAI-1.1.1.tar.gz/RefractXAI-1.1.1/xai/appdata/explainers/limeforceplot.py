import json
from .base import ModelInterpreter
from skater.core.local_interpretation.lime.lime_tabular import LimeTabularExplainer
from ..constants import Log
from ..logging import build_logger
import numpy as np

logger = build_logger(Log.logger_level, "fi")


class LimeForcePlot(ModelInterpreter):
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
        self.unique_values = tuple(map(lambda num: int(num), tuple(self.unique_values)))

        model_type = self.mode
        if model_type == "regression":
            self.lime_tab_exp = LimeTabularExplainer(
                training_data=self.x_train,
                feature_names=self.feature_names,
                class_names=self.target_names,
                verbose=True,
                mode='regression'
            )
        else:
           self.lime_tab_exp = LimeTabularExplainer(
            training_data=self.x_train,
            mode="classification",
            training_labels=self.y_train,
            feature_names=self.feature_names,
            categorical_features=None,
            categorical_names=None,
            kernel_width=None,
            verbose=False,
            class_names=self.unique_values,
            feature_selection='auto',
            discretize_continuous=True,
            discretizer='quartile'
        )


    def generate_data(self):
        """
            Generates the data for the Lime force plot importance.

            Returns:
                list: A list of dictionaries containing the lime data.

        """

        sample_rows = self.sample_rows
        lime_row_wise_data = {}
        # print(self.lime_tab_exp)
        if self.mode == "multiclassification" or self.mode == "binaryclassification":
            for row_num in sample_rows:
                sample_req = self.x_train[row_num]
                self.validate_sample_req()
                instance_data = self.lime_tab_exp.explain_instance(
                    data_row=sample_req,
                    predict_fn=self.model.predict_proba,
                    labels=self.unique_values,
                    top_labels=None,
                    num_features=10,
                    num_samples=5000,
                    distance_metric='euclidean',
                    model_regressor=None
                )
                temp = {}
                for i in range(len(instance_data.as_map())):
                    actualClasses = []
                    for dp in instance_data.class_names:
                        actualClasses.append(self.process_obj["labelInfo"][f"{dp}"])
                    classInfo = {
                        "list": {field: value for field, value in instance_data.as_list(i)},
                        "class": instance_data.class_names,
                        "predicted_value": {i: j for i, j in zip(actualClasses, instance_data.predict_proba.tolist())},
                        "mode": self.mode,
                        "intercept": instance_data.intercept,
                        "feature_values": [[i, j, "negative" if k[1] < 0 else "positive"] for i, j, k in zip(sample_req, self.feature_names, instance_data.as_map()[i])]
                    }
                    temp[self.process_obj["labelInfo"][f"{i}"]]=classInfo

                lime_row_wise_data[row_num] = temp

        if self.mode == "regression":
            for row_num in sample_rows:
                temp = {}
                sample_req = self.x_train[row_num]
                instance_data = self.lime_tab_exp.explain_instance(sample_req,self.model.predict, num_features=10)
                tempPercentage = {
                    "maxValue":instance_data.max_value,
                    "minValue":instance_data.min_value,
                    "predictedValue":instance_data.predicted_value
                }
                temp["predicted_value"] = tempPercentage

                feature_values=[[i, j, "negative" if k[1] < 0 else "positive"] for i, j, k in zip(sample_req, self.feature_names,instance_data.as_map()[1])]
                temp["feature_values"]=feature_values

                listInfo={field: value for field, value in instance_data.as_list(1)}
                temp["list"]=listInfo

                lime_row_wise_data[row_num] = temp
                lime_row_wise_data["regressionMode"] = "regression"
                lime_row_wise_data["target_name"] = self.target_names[0]
                

        return lime_row_wise_data


    def validate_sample_req(self):
        """
            Validates the sample request.

        """
        pass
        # import numpy as np
        # self.sample_req = np.array(self.sample_req)
        # if isinstance(self.sample_req, np.ndarray) and self.sample_req.shape[0] == len(self.feature_names):
        #     pass
        # else:
        #     raise ValueError("Sample request should be a numpy array for single row eg. np.array([1,2,3])")
