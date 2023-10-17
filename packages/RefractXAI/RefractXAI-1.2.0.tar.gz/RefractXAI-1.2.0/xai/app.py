
from utilities import ModelArtifacts,XAIHTML
import os,json
import numpy as np
from appdata.html_content import *
from appdata import ModelExplainer

def install_recipe_packages():
     pass


def get_basic_details():
        try:
                basic_details = json.loads(os.getenv("basic_details"))
                model_details = json.loads(os.getenv("model_details"))
                model_type = [item["field_value"] for item in basic_details if item["field_id"]=="problem_type"][0]
                model_flavour = [item["field_value"] for item in model_details if item["field_id"]=="model_flavour"][0]
                return {
                        "model_flavour" : model_flavour,
                        "model_type" : model_type
                }
        except Exception as msg:
                print(msg)
                raise Exception("Env details not found")

def main():
        
        basic_details = get_basic_details()
        model_path = "/models"
        model_flavour = basic_details["model_flavour"]
        output_path = os.getenv("output_path")
        class_mapping = None
        if "target_class_names" in os.environ:
                classe_names = os.getenv("target_class_names").strip().split(",")
                class_mapping = {str(index):value for index,value in enumerate(classe_names)}


        # import time
        # time.sleep(300)

        ## XAI Base HTML
        html_obj = XAIHTML(output_path,target_class_names=class_mapping)

        # Read Model Artifacts
        model_info = ModelArtifacts(model_path)
        model_artifacts = model_info.get_model_artifacts()

        # Install model dependencies
        model_info.install_model_dependencies()


        model = model_info.load_model(model_flavour)
        train_table = model_artifacts['x_train']
        test_table = model_artifacts['x_test']
        train_target = model_artifacts['y_train']
        test_target = model_artifacts['y_test']
        feature_names = model_artifacts['feature_names']
        target_names = model_artifacts['target_names']

        row_count = 100 if test_table.shape[0] > 100 else test_table.shape[0]

        train_table = train_table if type(train_table) == np.ndarray else train_table.to_numpy()
        train_target = train_target if type(train_target) == np.ndarray else train_target.to_numpy()
        test_table = test_table if type(test_table) == np.ndarray else test_table.to_numpy()
        test_target = test_target if type(test_target) == np.ndarray else test_target.to_numpy()

        model_type = basic_details["model_type"]
        if model_type == "binary_classification":
                model_type = "binaryclassification"
        elif model_type == "multiclass_classification":
                model_type = "multiclassification"
        else:
                model_type = "regression"
                
        process_obj = model_info.pickle_load_label_map(model_type)

        #sample rows for lime
        insert_random_rows_lime, indexs = insert_random_dataindexes(row_count,"lime")

        explainer = ModelExplainer(
                model=model,
                x_train=train_table,
                y_train=train_target,
                x_test=test_table,
                y_test=test_target,
                sample_rows=indexs,
                feature_names=feature_names,
                target_names=target_names,
                process_obj=process_obj,
                mode=model_type,
                feature_ids=None,
                preprocessing=None,
                sample_req=indexs,
                predict_fn=None
        )
        print("XAI started")
        # Feature Importance
        fi_data = explainer.fi.generate_data()
        multi_class_labels = load_multi_class_names(fi_data)
        html_feature_importance = get_html_feature_importance(fi_data)
        print("Completed Feature Importance")

        # Model Overview
        print("Started Model Overview")
        get_model_stats = explainer.ml_overview.generate_data()
        multi_class_labelsroc = load_multi_class_names_for_roc(get_model_stats) if not model_type=="regression" else None
        model_overview_html_script  = get_model_overview_html(get_model_stats,model_type)
        print("Completed Model Overview")

        # LimePlots
        lime_data = explainer.lf.generate_data()
        insert_multi_class_labels_lime,classnames = insert_class_labels_lime(lime_data)
        lime_plot_data = get_lime_html(lime_data,classnames)
        print("Completed LimePlots")

        # PDP
        pdp_data,target_labels,mode = explainer.pdp.generate_data()
        pdp_features_names,htmlClassLabels = insert_pdp_dropdown_list(feature_names,target_labels,mode)
        pdp_plot_data = get_pdp_html(pdp_data)
        print("Completed PDP")

        #Decision_plots
        dplot_data = explainer.dplot.generate_data()
        insert_dplot_rows,dplot_classes = insert_dplot_rows_class_info(dplot_data)
        dplot_explainer_html = insert_dplot_plot(dplot_data)
        print("Completed Decision Plots")

        html_params_list = [
        ("feature_importance",html_feature_importance),
        ("multi_class_labels",multi_class_labels),
        ("multi_class_labelsroc",multi_class_labelsroc),
        ("model_overview_html_script",model_overview_html_script),
        ("insert_random_rows_lime",insert_random_rows_lime),
        ("insert_multi_class_labels_lime",insert_multi_class_labels_lime),
        ("lime_plot_data",lime_plot_data),
        ("pdp_features_names",pdp_features_names),
        ("htmlClassLabelsPDP",htmlClassLabels),
        ("pdp_plot_data",pdp_plot_data),
        ("insert_dplot_rows",insert_dplot_rows),
        ("insert_dplot_classes",dplot_classes),
        ("dplot_explainer_html",dplot_explainer_html)
        ]


        json_params_list = [
                        ("feature_importance",fi_data),
                        ("model_stats",{key:value for key,value in get_model_stats.items() if not key=="confusion_matrix_ui"}),
                        ("lime_data",lime_data),
                        ("partial_dependence_plot_data",pdp_data),
                        ("decision_plot_data",dplot_data)
        ]



        html_obj.load_html(**dict(html_params_list))

        html_obj.save_json_file(**dict(json_params_list))
            
if __name__ == "__main__":
        main()
