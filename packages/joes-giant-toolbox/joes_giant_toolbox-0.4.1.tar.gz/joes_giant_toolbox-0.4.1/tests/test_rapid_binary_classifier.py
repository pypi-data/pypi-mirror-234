# import sys
# import pathlib
# import pathlib
# import subprocess
# import pandas as pd
# import sklearn
# import sklearn.preprocessing
# import sklearn.model_selection
# import sklearn.naive_bayes
# import sklearn.tree
# import sklearn.linear_model
# import sklearn.neural_network
# import sklearn.discriminant_analysis
# import sklearn.ensemble
# import sklearn.gaussian_process
# import sklearn.metrics
# import sklearn.calibration
# from matplotlib import pyplot as plt

# # add the root project directory to the system path #
# parent_dir_path = pathlib.Path(__file__).parent.parent
# sys.path.append(str(parent_dir_path))

# # import the function to be tested:
# from joes_giant_toolbox.rapid_binary_classifier import RapidBinaryClassifier

# # run the tests #
# def test_good_performance_cleveland_heart_disease_dataset():
#     """This test checks that the process can produce a model which achieves an ROC/AUC score of at least 0.85 on the Cleveland Heart Dataset:

#     1. Using the methods in the class directly
#     2. Exporting the full auto-generated script and running it
#     """
#     data_df = pd.read_csv(
#         "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
#         sep=",",
#         header=None,
#         names=[
#             "age",
#             "sex",
#             "chest_pain_type",
#             "resting_blood_pressure",
#             "serum_cholesterol_mg_dl",
#             "fasting_blood_sugar",
#             "resting_electrocardiographic_results",
#             "maximum_heart_rate_achieved",
#             "exercise_induced_angina",
#             "st_depression_induced_by_exercise_relative_to_rest",
#             "slope_of_peak_exercise_st_segment",
#             "num_major_vessels_colored_by_flourosopy",
#             "thal",
#             "angiographic_disease_status",
#         ],
#         dtype=float,
#         skiprows=[87, 166, 192, 266, 287, 302],  # rows with missing values
#     )
#     data_df["heart_disease_yes_no"] = (
#         data_df["angiographic_disease_status"] > 0
#     ).astype(int)
#     # data_df.nunique()
#     sk_classifier = RapidBinaryClassifier(
#         data_df=data_df, verbose=False, eval_code=True
#     )
#     sk_classifier.set_variable_roles_in_model(
#         y_varname="heart_disease_yes_no",
#         x_numeric_varnames=[
#             "age",
#             "resting_blood_pressure",
#             "serum_cholesterol_mg_dl",
#             "maximum_heart_rate_achieved",
#             "st_depression_induced_by_exercise_relative_to_rest",
#         ],
#         x_categorical_varnames=[
#             "sex",
#             "chest_pain_type",
#             "fasting_blood_sugar",
#             "resting_electrocardiographic_results",
#             "exercise_induced_angina",
#             "slope_of_peak_exercise_st_segment",
#             "num_major_vessels_colored_by_flourosopy",
#             "thal",
#         ],
#     )
#     sk_classifier.generate_train_test_split(test_percent=0.2)
#     sk_classifier.transform_x_features(rare_category_min_freq=20)
#     sk_classifier.define_models(
#         {
#             "adaboost": sklearn.ensemble.AdaBoostClassifier(),
#             "decision_tree": sklearn.tree.DecisionTreeClassifier(),
#             "extremely_random_trees": sklearn.ensemble.ExtraTreesClassifier(),
#             "gaussian_naive_bayes": sklearn.naive_bayes.GaussianNB(),
#             "gaussian_process": sklearn.gaussian_process.GaussianProcessClassifier(),
#             "hist_gbm": sklearn.ensemble.HistGradientBoostingClassifier(),
#             "logistic_regression": sklearn.linear_model.LogisticRegression(
#                 penalty=None,
#                 max_iter=1_000,
#             ),
#             "neural_net": sklearn.neural_network.MLPClassifier(
#                 hidden_layer_sizes=(50, 30, 10, 5), activation="relu", max_iter=1_000
#             ),
#             "quadratic_discriminant_analysis": sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis(),
#             "random_forest": sklearn.ensemble.RandomForestClassifier(),
#         }
#     )
#     all_model_names = list(sk_classifier.sklearn_components["models"].keys())
#     sk_classifier.fit_cross_valid_models(
#         k_folds=4,
#         model_names_list=all_model_names,
#     )
#     # sk_classifier.compare_models_cross_valid_roc_auc()
#     sk_classifier.add_ensemble_model(
#         ensemble_name="weighted_avg_ensemble_all_models",
#         model_names_list=all_model_names,
#         combine_strategy="weighted_average",
#     )
#     sk_classifier.add_ensemble_model(
#         ensemble_name="stacked_classifier_ensemble_all_models",
#         model_names_list=all_model_names,
#         combine_strategy="stacked_classifier",
#         meta_model=sklearn.ensemble.HistGradientBoostingClassifier(),
#     )
#     sk_classifier.fit_cross_valid_models(
#         k_folds=4,
#         model_names_list=[
#             "weighted_avg_ensemble_all_models",
#             "stacked_classifier_ensemble_all_models",
#         ],
#     )
#     per_model_mean_cross_valid_test_score = {
#         model_name: sk_classifier.sklearn_components["k_fold_cv_results"][model_name][
#             "test_score"
#         ].mean()
#         for model_name in sk_classifier.sklearn_components["k_fold_cv_results"]
#     }
#     best_model_name_cross_valid_test = max(
#         per_model_mean_cross_valid_test_score,
#         key=per_model_mean_cross_valid_test_score.get,
#     )
#     # sk_classifier.compare_models_cross_valid_roc_auc()
#     sk_classifier.fit_models(model_names_list=[best_model_name_cross_valid_test])
#     sk_classifier.generate_test_set_predictions(
#         model_names_list=[best_model_name_cross_valid_test]
#     )
#     test_data_roc_auc = sklearn.metrics.roc_auc_score(
#         y_true=sk_classifier.data["y_test_for_model"],
#         y_score=sk_classifier.sklearn_components["test_set_predictions"][
#             best_model_name_cross_valid_test
#         ],
#     )

#     assert (
#         test_data_roc_auc >= 0.85
#     ), f"Best model ({best_model_name_cross_valid_test}) achieved roc_auc={test_data_roc_auc:.3f} on Cleveland Heart Dataset (test partition) - should achieve at least 0.85"

#     edit_full_model_script = (
#         sk_classifier.full_model_script.replace(
#             r"data_df = pd.read_csv(...)",
#             r"""data_df = pd.read_csv(
#         "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
#         sep=",",
#         header=None,
#         names=[
#             "age",
#             "sex",
#             "chest_pain_type",
#             "resting_blood_pressure",
#             "serum_cholesterol_mg_dl",
#             "fasting_blood_sugar",
#             "resting_electrocardiographic_results",
#             "maximum_heart_rate_achieved",
#             "exercise_induced_angina",
#             "st_depression_induced_by_exercise_relative_to_rest",
#             "slope_of_peak_exercise_st_segment",
#             "num_major_vessels_colored_by_flourosopy",
#             "thal",
#             "angiographic_disease_status",
#         ],
#         dtype=float,
#         skiprows=[87, 166, 192, 266, 287, 302],  # rows with missing values
# )
# data_df["heart_disease_yes_no"] = (data_df["angiographic_disease_status"] > 0).astype(int)""",
#         )
#         + f"""
# test_data_roc_auc = sklearn.metrics.roc_auc_score(
#     y_true=y_test_for_model,
#     y_score=test_data_predictions[models_to_predict_list[0]],
# )
# with open("temp_external_script_output.txt", "w") as f:
#         f.write(f"{{models_to_predict_list[0]}}{{chr(10)}}")
#         f.write(f"{{test_data_roc_auc:.3f}}")
#     """
#     )
#     try:
#         with open("temp_model_script.py", "w") as f:
#             f.write(edit_full_model_script)
#         subprocess.run(["python", "temp_model_script.py"])
#         with open("temp_external_script_output.txt", "r") as f:
#             external_script_output_list = [x.strip() for x in f.readlines()]
#         best_external_model_name = external_script_output_list[0]
#         external_best_roc_auc = float(external_script_output_list[1])
#         assert (
#             external_best_roc_auc >= 0.85
#         ), f"External script best model ({best_external_model_name}) achieved roc_auc={external_best_roc_auc} on Cleveland Heart Dataset (test partition) - should achieve at least 0.85"
#     except:
#         pass
#     finally:
#         for filename in ["temp_external_script_output.txt", "temp_model_script.py"]:
#             pathlib.Path(filename).unlink(missing_ok=True)
