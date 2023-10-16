from typing import List
import warnings
import time
import pandas as pd
import numpy as np
import sklearn
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.tree
import sklearn.linear_model
import sklearn.neural_network
import sklearn.discriminant_analysis
import sklearn.ensemble
import sklearn.gaussian_process
import sklearn.metrics
import sklearn.calibration
from matplotlib import pyplot as plt


class RapidBinaryClassifier:
    """Facilitates the ultra rapid generation of binary classifier models in scikit-learn by abstracting away a lot of the decisions and model code

    Notes
    -----
    This class is useful for quickly assessing the feasibility of supervised learning for a particular problem
    It provides a quick baseline level of model performance
    It also provides a lot of boilerplate scikit-learn code, which is a convenient starting point for a project (much easier than coding from scratch)
    The Scikit-Learn gitHub repo is at "https://github.com/scikit-learn/scikit-learn"

    Future Additions (not yet implemented)
    --------------------------------------
    * Missing data imputation
    * Feature selection (including removal of collinear features)
    * More model understanding:
        - Feature Explainability (feature importance, partial dependence plots, SHAP values etc.)
    * Hyperparameter tuning (probably using Optuna)
    * Additional models e.g. Tensorflow, Pytorch, CatBoost, LightGBM, XG-Boost
    * Make the automatically generated code more beautiful (clean up variable naming etc.)

    Example Usage
    -------------
    >>> data_df = pd.read_csv(
    ...     "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    ...     header=None,
    ...     names=["age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","native-country","annual_salary"],
    ... ).sample(5_000)
    >>> data_df["annual_salary_over_50k"] = (data_df["annual_salary"] == " >50K").astype(int)
    >>> sk_classifier = RapidBinaryClassifier(data_df=data_df, verbose=True, eval_code=True)
    >>> sk_classifier.assess_input_data_quality()
    >>> sk_classifier.set_variable_roles_in_model(
    ...    y_varname="annual_salary_over_50k",
    ...    x_numeric_varnames=[
    ...        "age",
    ...        "fnlwgt",
    ...        "education-num",
    ...        "capital-gain",
    ...        "capital-loss",
    ...        "hours-per-week",
    ...    ],
    ...    x_categorical_varnames=[
    ...        "workclass",
    ...        "education",
    ...        "marital-status",
    ...        "occupation",
    ...        "relationship",
    ...        "race",
    ...        "sex",
    ...        "native-country",
    ...    ],
    ... )
    >>> sk_classifier.generate_train_test_split(test_percent=0.2)
    >>> sk_classifier.transform_x_features(rare_category_min_freq=250)
    >>> sk_classifier.define_models(
    ...     {
    ...         "adaboost": sklearn.ensemble.AdaBoostClassifier(),
    ...         "decision_tree": sklearn.tree.DecisionTreeClassifier(),
    ...         "extremely_random_trees": sklearn.ensemble.ExtraTreesClassifier(),
    ...         "gaussian_naive_bayes": sklearn.naive_bayes.GaussianNB(),
    ...         # "gaussian_process": sklearn.gaussian_process.GaussianProcessClassifier(),
    ...         "hist_gbm": sklearn.ensemble.HistGradientBoostingClassifier(),
    ...         "logistic_regression": sklearn.linear_model.LogisticRegression(
    ...             penalty=None,
    ...             max_iter=1_000,
    ...         ),
    ...         "neural_net": sklearn.neural_network.MLPClassifier(
    ...             hidden_layer_sizes=(50, 30, 10, 5), activation="relu", max_iter=1_000
    ...         ),
    ...         "quadratic_discriminant_analysis": sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis(),
    ...         "random_forest": sklearn.ensemble.RandomForestClassifier(),
    ...     }
    ... )
    >>> all_model_names = list(sk_classifier.sklearn_components["models"].keys())
    >>> sk_classifier.fit_cross_valid_models(
    ...     k_folds=10,
    ...     model_names_list=all_model_names,
    ... )
    >>> sk_classifier.compare_models_cross_valid_roc_auc()
    >>> sk_classifier.add_ensemble_model(
    ...     ensemble_name="weighted_avg_ensemble_all_models",
    ...     model_names_list=all_model_names,
    ...     combine_strategy="weighted_average",
    ... )
    >>> sk_classifier.add_ensemble_model(
    ...     ensemble_name="weighted_avg_ensemble_best_models",
    ...     model_names_list=[
    ...         "adaboost",
    ...         "hist_gbm",
    ...         "logistic_regression",
    ...         "random_forest",
    ...     ],
    ...     combine_strategy="weighted_average",
    ... )
    >>> sk_classifier.add_ensemble_model(
    ...     ensemble_name="stacked_classifier_ensemble_all_models",
    ...     model_names_list=all_model_names,
    ...     combine_strategy="stacked_classifier",
    ...     meta_model=sklearn.ensemble.HistGradientBoostingClassifier(),
    ... )
    >>> sk_classifier.fit_cross_valid_models(
    ...     k_folds=10,
    ...     model_names_list=[
    ...         "weighted_avg_ensemble_all_models",
    ...         "weighted_avg_ensemble_best_models",
    ...         "stacked_classifier_ensemble_all_models",
    ...     ],
    ... )
    >>> sk_classifier.compare_models_cross_valid_roc_auc()
    >>> final_chosen_model_names_list = [
    ...     "adaboost",
    ...     "hist_gbm",
    ...     "logistic_regression",
    ...     "weighted_avg_ensemble_best_models",
    ...     "stacked_classifier_ensemble_all_models",
    ... ]
    >>> sk_classifier.fit_models(model_names_list=final_chosen_model_names_list)
    >>> sk_classifier.generate_test_set_predictions(
    ...    model_names_list=final_chosen_model_names_list
    ... )
    >>> sk_classifier.compare_models_test_set_roc_curves(model_names_list=final_chosen_model_names_list)
    >>> sk_classifier.compare_models_calibration_test_set(model_names_list=final_chosen_model_names_list, n_bins=10)
    >>> sk_classifier.compare_models_test_set_precision_recall(model_names_list=final_chosen_model_names_list)
    """

    def __init__(self, data_df: pd.DataFrame, verbose: bool, eval_code: bool) -> None:
        self.global_params = {
            "verbose": verbose,
            "eval_code": eval_code,
        }
        self.data = {
            "data_df": data_df.copy(),
            "y": None,
            "x_df": None,
            "y_train_for_model": None,
            "y_test_for_model": None,
            "x_train": None,
            "x_test": None,
            "x_train_categorical_1hot": None,
            "x_test_categorical_1hot": None,
            "x_train_numeric": None,
            "x_test_numeric": None,
            "x_train_for_model": None,
            "x_test_for_model": None,
        }
        self.user_inputs = {
            "x_numeric_varnames": [],
            "x_categorical_varnames": [],
        }
        self.sklearn_components = {
            "feature_engineering": {"one_hot_transformer": None},
            "models": {},
            "k_folds": None,
            "k_fold_cv_results": {},
            "test_set_predictions": {},
        }
        self.full_model_script = """
# import packages #
import time
import pandas as pd
import numpy as np
import sklearn
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.tree
import sklearn.linear_model
import sklearn.neural_network
import sklearn.discriminant_analysis
import sklearn.ensemble
import sklearn.gaussian_process
import sklearn.metrics
import sklearn.calibration
from matplotlib import pyplot as plt
        """
        self.full_model_script += """
# import data #
data_df = pd.read_csv(...)
        """
        if self.global_params["verbose"]:
            print(self.full_model_script)

    def assess_input_data_quality(self) -> None:
        """Checks the quality of the raw input data self.data["data_df"]"""
        code_str = f"""
# Quantify missing values in input data #
print("Count of missing values per column:")
print(data_df.isna().sum())
assert data_df.isna().sum().sum() == 0, "Missing values in input data currently not supported"
"""
        self.full_model_script += code_str
        if self.global_params["verbose"]:
            print(code_str)
        if self.global_params["eval_code"]:
            print("Count of missing values per column:")
            print(self.data["data_df"].isna().sum())
            assert (
                self.data["data_df"].isna().sum().sum() == 0
            ), "Missing values in input data currently not supported (future version will include missing data imputation)"
            warnings.warn(
                "Missing value imputation is not yet implemented - input data must have no missing values",
                UserWarning,
            )

    def set_variable_roles_in_model(
        self,
        y_varname: str,
        x_numeric_varnames: List[str],
        x_categorical_varnames: List[str],
    ) -> None:
        """Specifies which variables are to be included in the model, and the role of each

        Parameters
        ----------
        y_varname: str
            The column name of the outcome variable (binary variable to be predicted)
        x_numeric_varnames: List[str]
            List of column names of continuous (real-values) variables to included as predictors in the model
        x_categorical_varnames: List[str]
            List of column names of categorical variables to be included as predictors in the model
        """
        code_str = f"""
# define variable roles in model #
y = data_df["{y_varname}"]
x_numeric_varnames = [{",".join([f'"{x}"'for x in x_numeric_varnames])}]
x_categorical_varnames = [{",".join([f'"{x}"'for x in x_categorical_varnames])}]
x_df = data_df[x_numeric_varnames + x_categorical_varnames]
"""
        self.full_model_script += code_str
        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            self.data["y"] = self.data["data_df"][y_varname]
            self.user_inputs["x_numeric_varnames"] = x_numeric_varnames
            self.user_inputs["x_categorical_varnames"] = x_categorical_varnames
            self.data["x_df"] = self.data["data_df"][
                x_numeric_varnames + x_categorical_varnames
            ]

    def generate_train_test_split(self, test_percent: float) -> None:
        """Splits data into 2 non-overlapping partitions ("training" and "test")

        Parameters
        ----------
        test_percent: float in (0.0, 1.0)
            Proportion of the input data to include in the test partition
            The training partition is then 100(1-test_percent)% of the input data
        """
        code_str = f"""
# train/test split #
train_percent = {1.0-test_percent}
test_percent = {test_percent}
x_train, x_test, y_train_for_model, y_test_for_model = sklearn.model_selection.train_test_split(
        x_df, y, test_size=test_percent
)
        """
        self.full_model_script += code_str
        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            (
                self.data["x_train"],
                self.data["x_test"],
                self.data["y_train_for_model"],
                self.data["y_test_for_model"],
            ) = sklearn.model_selection.train_test_split(
                self.data["x_df"], self.data["y"], test_size=test_percent
            )

    def transform_x_features(self, rare_category_min_freq: int) -> None:
        """1-hot encodes categorical predictors and scales numeric predictors

        Parameters
        ----------
        rare_category_min_freq: int
            (only applies to categorical predictors)
            Categories must have at least this many samples, otherwise they are put into the category "infrequent_sklearn"
        """
        code_str = f"""
# feature preprocessing #
one_hot_var_transformer = sklearn.preprocessing.OneHotEncoder(
    sparse_output=False,  # return output as sparse array
    handle_unknown="ignore",  # ignore levels (categories) unseen in training data
    min_frequency={rare_category_min_freq},  # categories with fewer samples will be labelled "infrequent_sklearn"
    dtype=np.int8,  # Data type of output columns
)

numeric_scaler_transformer = sklearn.preprocessing.StandardScaler()

one_hot_var_transformer.fit( x_train[x_categorical_varnames] )
numeric_scaler_transformer.fit( x_train[x_numeric_varnames] )

x_train_categorical_1hot = pd.DataFrame(
    one_hot_var_transformer.transform( x_train[x_categorical_varnames] ),
    columns = one_hot_var_transformer.get_feature_names_out(),
)
x_test_categorical_1hot = pd.DataFrame(
    one_hot_var_transformer.transform( x_test[x_categorical_varnames] ),
    columns = one_hot_var_transformer.get_feature_names_out(),
)

x_train_numeric = pd.DataFrame(
    numeric_scaler_transformer.transform( x_train[x_numeric_varnames] ),
    columns = numeric_scaler_transformer.get_feature_names_out(),
)
x_test_numeric = pd.DataFrame(
    numeric_scaler_transformer.transform( x_test[x_numeric_varnames] ),
    columns = numeric_scaler_transformer.get_feature_names_out(),
)

x_train_for_model = pd.concat( [x_train_categorical_1hot, x_train_numeric], axis=1 )
x_test_for_model = pd.concat( [x_test_categorical_1hot, x_test_numeric], axis=1 )
"""
        self.full_model_script += code_str
        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            one_hot_var_transformer = sklearn.preprocessing.OneHotEncoder(
                sparse_output=False,  # return output as sparse array
                handle_unknown="ignore",  # ignore levels (categories) unseen in training data
                min_frequency=rare_category_min_freq,  # categories with fewer samples will be labelled "infrequent_sklearn"
                dtype=np.int8,  # Data type of output columns
            )

            numeric_scaler_transformer = sklearn.preprocessing.StandardScaler()

            one_hot_var_transformer.fit(
                self.data["x_train"][self.user_inputs["x_categorical_varnames"]]
            )
            numeric_scaler_transformer.fit(
                self.data["x_train"][self.user_inputs["x_numeric_varnames"]]
            )

            self.sklearn_components["feature_engineering"][
                "one_hot_transformer"
            ] = one_hot_var_transformer
            self.sklearn_components["feature_engineering"][
                "numeric_scaler_transformer"
            ] = numeric_scaler_transformer

            self.data["x_train_categorical_1hot"] = pd.DataFrame(
                one_hot_var_transformer.transform(
                    self.data["x_train"][self.user_inputs["x_categorical_varnames"]]
                ),
                columns=one_hot_var_transformer.get_feature_names_out(),
            )
            self.data["x_test_categorical_1hot"] = pd.DataFrame(
                one_hot_var_transformer.transform(
                    self.data["x_test"][self.user_inputs["x_categorical_varnames"]]
                ),
                columns=one_hot_var_transformer.get_feature_names_out(),
            )

            self.data["x_train_numeric"] = pd.DataFrame(
                numeric_scaler_transformer.transform(
                    self.data["x_train"][self.user_inputs["x_numeric_varnames"]]
                ),
                columns=numeric_scaler_transformer.get_feature_names_out(),
            )
            self.data["x_test_numeric"] = pd.DataFrame(
                numeric_scaler_transformer.transform(
                    self.data["x_test"][self.user_inputs["x_numeric_varnames"]]
                ),
                columns=numeric_scaler_transformer.get_feature_names_out(),
            )

            self.data["x_train_for_model"] = pd.concat(
                [
                    self.data["x_train_categorical_1hot"],
                    self.data["x_train_numeric"],
                ],
                axis=1,
            )
            self.data["x_test_for_model"] = pd.concat(
                [
                    self.data["x_test_categorical_1hot"],
                    self.data["x_test_numeric"],
                ],
                axis=1,
            )

    def define_models(self, models_dict: dict) -> None:
        """Initiates the sklearn models to be fit

        Parameters
        ----------
        models_dict: dict
            A dictionary containing the sklearn models to be fit

        Example Usage
        -------------
        >>>sk_classifier = RapidBinaryClassifier(data_df=data_df, verbose=True, eval_code=True)
        >>>sk_classifier.define_models(
        ...     models_dict = {
        ...         "adaboost": sklearn.ensemble.AdaBoostClassifier(),
        ...         "logistic_regression": sklearn.linear_model.LogisticRegression(
        ...             penalty=None,
        ...             max_iter=1_000,
        ...         )
        ...     }
        ... )
        """
        code_str = """
# define models #
models_dict = {
"""
        for model_name in models_dict:
            code_str += f"\t\"{model_name}\": {'.'.join(models_dict[model_name].__module__.split('.')[:2])}.{models_dict[model_name]},\n"
            # code_str += f"\t\"{model_name}\": {'.'.join(models_dict[model_name].__module__.split('.')[:2])}.{models_dict[model_name].__class__.__name__}(),\n"
        code_str += """}
k_fold_cv_results_dict = {}
"""

        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            self.sklearn_components["models"] = models_dict

    def fit_cross_valid_models(self, model_names_list: List[str], k_folds: int) -> None:
        """Estimates out-of-sample performance (ROC AUC) of each model using k-Fold Cross Validation (i.e. each model is trained from scratch k times)

        Parameters
        ----------
        model_names_list: List[str]
            List of models to be fit (list of model names)
            Note that the name format must match the format of the model names given previously in the define_models() function
        k_folds: int
            The number of folds to create for k-Fold Cross Validation
        """
        self.sklearn_components["k_folds"] = k_folds

        code_str = f"""
# run {k_folds}-fold cross validation #
model_fit_counter = 1
cv_model_names_list = {model_names_list} 
for model_name in cv_model_names_list:
    start_time = time.perf_counter()
    print(
        f"fitting model {{model_fit_counter}} of {{len(cv_model_names_list)}} [{{model_name}}] ({k_folds} folds)..",
        end="",
    )
    k_fold_cv_results_dict[model_name] = sklearn.model_selection.cross_validate(
        estimator=sklearn.base.clone(models_dict[model_name]),
        X=x_train_for_model,
        y=y_train_for_model,
        scoring="roc_auc",
        cv={k_folds},
        return_train_score=True,
        return_estimator=False,
    )
    minutes_elapsed = (time.perf_counter() - start_time) / 60
    print(f"..done ({{minutes_elapsed:.2f}} minutes)")
    model_fit_counter += 1
"""
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            model_fit_counter = 1
            for model_name in model_names_list:
                start_time = time.perf_counter()
                print(
                    f"fitting model {model_fit_counter} of {len(model_names_list)} [{model_name}] ({k_folds} folds)..",
                    end="",
                )
                self.sklearn_components["k_fold_cv_results"][
                    model_name
                ] = sklearn.model_selection.cross_validate(
                    estimator=sklearn.base.clone(
                        self.sklearn_components["models"][model_name]
                    ),
                    X=self.data["x_train_for_model"],
                    y=self.data["y_train_for_model"],
                    scoring="roc_auc",
                    cv=k_folds,
                    return_train_score=True,
                    return_estimator=False,
                )
                minutes_elapsed = (time.perf_counter() - start_time) / 60
                print(f"..done ({minutes_elapsed:.2f} minutes)")
                model_fit_counter += 1

    def compare_models_cross_valid_roc_auc(self) -> None:
        """Plots the ROC AUC Score achieved by each model on each Cross Validation Fold"""

        code_str = f"""
# compare model cross-validation performance (ROC AUC) #
x_axis_values = []
y_axis_values = []
model_counter = 0
cv_model_names_list = list(k_fold_cv_results_dict.keys())
for model_name in cv_model_names_list:
    test_score_each_fold = k_fold_cv_results_dict[model_name]["test_score"].tolist()
    x_axis_values += [model_counter] * len(test_score_each_fold)
    y_axis_values += test_score_each_fold
    model_counter += 1

plt.figure(figsize=(10, 5))
plt.scatter(x_axis_values, y_axis_values, alpha=0.5)
plt.xticks(ticks=range(len(cv_model_names_list)), labels=cv_model_names_list, rotation=90)
plt.xlabel("Model Name")
plt.ylabel("ROC AUC")
plt.title(
    f"Model Performance (ROC AUC) on Each Test Fold Using {self.sklearn_components['k_folds']}-Fold Cross Validation"
)
plt.show()
"""
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            x_axis_values = []
            y_axis_values = []
            model_counter = 0
            model_names = list(self.sklearn_components["k_fold_cv_results"].keys())
            for model_name in model_names:
                test_score_each_fold = self.sklearn_components["k_fold_cv_results"][
                    model_name
                ]["test_score"].tolist()
                x_axis_values += [model_counter] * len(test_score_each_fold)
                y_axis_values += test_score_each_fold
                model_counter += 1
            plt.figure(figsize=(10, 5))
            plt.scatter(x_axis_values, y_axis_values, alpha=0.5)
            plt.xticks(ticks=range(len(model_names)), labels=model_names, rotation=90)
            plt.xlabel("Model Name")
            plt.ylabel("ROC AUC")
            plt.title(
                f"Model Performance (ROC AUC) on Each Test Fold Using {self.sklearn_components['k_folds']}-Fold Cross Validation"
            )
            plt.show()

    def add_ensemble_model(
        self,
        ensemble_name: str,
        model_names_list: List[str],
        combine_strategy: str,
        meta_model=None,
    ) -> None:
        """Add a new composite model which combines the predictions of multiple component models

        Parameters
        ----------
        ensemble_name: str
            The name which will be used to identify the model at later stages of the modelling process
        model_names_list: List[str]
            The list of models to include in the ensemble
            Note that the name format must match the format of the model names given previously in the define_models() function
        combine_strategy: str, one of {"weighted_average","stacked_classifier"}
            The strategy to use for combining the predictions of the component models in the ensemble
                * "weighted_average" creates a combined prediction by averaging the scores of the component models, where the weights are relative to the models' cross validation performance
                * "stacked_classifier" uses the component models' predictions as features and trains a new model using these features
        meta_model, default=None
            A SciKit-Learn model object
            This parameter is ignored if combine_strategy="weighted_average"
            This model is used as the meta-model, combining the predictions of the component models in order to generate a single prediction per sample
        """
        if combine_strategy == "stacked_classifier":
            code_str = f"""
\n# create (stacked classifier) ensemble model [{ensemble_name}] #            
models_in_ensemble = {model_names_list}
models_dict["{ensemble_name}"] = sklearn.ensemble.StackingClassifier(
    estimators=[
                    (
                        model_name,
                        sklearn.base.clone(
                            models_dict[model_name]
                        ),
                    )
                    for model_name in models_in_ensemble
                ],
                final_estimator={'.'.join(meta_model.__module__.split('.')[:2])}.{meta_model},
                cv=5,
                stack_method="predict_proba",
                n_jobs=-1,
                passthrough=True,
            )            
            """
        elif combine_strategy == "weighted_average":
            code_str = f"""
\n# create (weighted average) ensemble model [{ensemble_name}] #                       
models_in_ensemble = {model_names_list}
mean_cv_performance_test_fold = [k_fold_cv_results_dict[model_name]["test_score"].mean() for model_name in {model_names_list}]        
models_dict["{ensemble_name}"] = sklearn.ensemble.VotingClassifier(
    estimators=[    
                (
                    model_name,
                        sklearn.base.clone(
                            models_dict[model_name]
                        ),
                    )
                    for model_name in models_in_ensemble
                ],
                voting="soft",
                weights=[
                    x / sum(mean_cv_performance_test_fold)
                    for x in mean_cv_performance_test_fold
                ],
)  
            """
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            if combine_strategy == "stacked_classifier":
                self.sklearn_components["models"][
                    ensemble_name
                ] = sklearn.ensemble.StackingClassifier(
                    estimators=[
                        (
                            model_name,
                            sklearn.base.clone(
                                self.sklearn_components["models"][model_name]
                            ),
                        )
                        for model_name in model_names_list
                    ],
                    final_estimator=meta_model,
                    cv=5,
                    stack_method="predict_proba",
                    n_jobs=-1,
                    passthrough=True,
                )
            elif combine_strategy == "weighted_average":
                mean_cv_performance_test_fold = [
                    self.sklearn_components["k_fold_cv_results"][model_name][
                        "test_score"
                    ].mean()
                    for model_name in model_names_list
                ]

                self.sklearn_components["models"][
                    ensemble_name
                ] = sklearn.ensemble.VotingClassifier(
                    estimators=[
                        (
                            model_name,
                            sklearn.base.clone(
                                self.sklearn_components["models"][model_name]
                            ),
                        )
                        for model_name in model_names_list
                    ],
                    voting="soft",
                    weights=[
                        x / sum(mean_cv_performance_test_fold)
                        for x in mean_cv_performance_test_fold
                    ],
                )

    def fit_models(self, model_names_list: List[str]) -> None:
        """Fit (train) selected models on the full training data

        Parameters
        ----------
        model_names_list: List[str]
            The list of models to train (list of model names)
            Note that the model name format must match the format of the model names given previously in the define_models() function
        """
        code_str = f"""
# Train models on full training dataset #
models_to_train_list = {model_names_list}  
for model_name in models_to_train_list:
    print(f"fitting model '{{model_name}}'..", end="")
    start_time = time.perf_counter()
    models_dict[model_name].fit(
        X=x_train_for_model, 
        y=y_train_for_model,
    )
    minutes_elapsed = (time.perf_counter() - start_time) / 60
    print(f"..done ({{minutes_elapsed:.2f}} minutes)")         
"""
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            for model_name in model_names_list:
                print(f"fitting model '{model_name}'..", end="")
                start_time = time.perf_counter()
                self.sklearn_components["models"][model_name].fit(
                    X=self.data["x_train_for_model"], y=self.data["y_train_for_model"]
                )
                minutes_elapsed = (time.perf_counter() - start_time) / 60
                print(f"..done ({minutes_elapsed:.2f} minutes)")

    def generate_test_set_predictions(self, model_names_list: List[str]) -> None:
        """Generate model predictions on the test data partition

        Parameters
        ----------
        model_names_list: List[str]
            List of models for which to generate predictions
            Note that the model name format must match the format of the model names given previously in the define_models() function
        """
        code_str = f"""
# generate model predictions on test data #
models_to_predict_list = {model_names_list}
test_data_predictions = {{}}
for model_name in models_to_predict_list:
    test_data_predictions[model_name] = models_dict[model_name].predict_proba(
        X = x_test_for_model
    )[:, 1]
"""

        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            for model_name in model_names_list:
                self.sklearn_components["test_set_predictions"][
                    model_name
                ] = self.sklearn_components["models"][model_name].predict_proba(
                    X=self.data["x_test_for_model"]
                )[
                    :, 1
                ]

    def compare_models_test_set_roc_curves(self, model_names_list: List[str]) -> None:
        """Plot ROC curve for each model using their test data predictions

        Parameters
        ----------
        model_names_list: List[str]
            List of models to include in the plot (list of model names)
            Note that the model name format must match the format of the model names given previously in the define_models() function
        """
        roc_curve_explanation_text = """
-- Explanation of ROC Curve --
TPR = "True Positive Rate" = "Recall" = The proportion of true y=1 cases which the model has correctly labelled as y=1
FPR = "False Positive Rate" = The proportion of y=0 cases which the model incorrectly labelled as y=1
        
The ROC Curve plots the TPR and FPR achieved under a range of different "decision thresholds" (between 0.0 and 1.0)
For a given "decision threshold", all samples with estimated Pr[y=1] higher than that threshold are labelled as the positive (y=1) class
        
A good resource: https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc        
        """
        code_str = f"""
# compare models performance on test data: ROC curves #
\"\"\"
{roc_curve_explanation_text}
\"\"\"
roc_curve_data = {{}}
roc_auc_scores = {{}}
model_names_list = {model_names_list}
for model_name in model_names_list:
    model_pred_y = test_data_predictions[model_name]
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(
        y_true=y_test_for_model,
        y_score=model_pred_y,
    )
    roc_curve_data[model_name] = {{
        "fpr": fpr,
        "tpr": tpr,
        "thresholds": thresholds,
    }}
    roc_auc_scores[model_name] = sklearn.metrics.roc_auc_score(
        y_true=y_test_for_model, y_score=model_pred_y
    )
roc_auc_scores = dict(
    sorted(roc_auc_scores.items(), key=lambda item: item[1], reverse=True)
)
print(\"\"\"--ROC AUC Scores (test data)--
The "ROC AUC Score" is the area under the ROC Curve (a value between 0.0 and 1.0)
It is also the probability that a randomly drawn positive (y=1) case and negative (y=0) case are ranked correctly by the model 
\"\"\"
)
for model_name in roc_auc_scores:
    print(f"\t{{model_name}}: {{roc_auc_scores[model_name]:.2f}}")

plt.figure(figsize=(10, 7))
for model_name in roc_curve_data:
    plt.plot(
        roc_curve_data[model_name]["fpr"],
        roc_curve_data[model_name]["tpr"],
        label=model_name,
    )
plt.axline([0, 0], [1, 1])
plt.legend()
plt.title("ROC Curves (Test Data)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate (Recall)")
[plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
[plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
plt.show()
"""
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            print(roc_curve_explanation_text)
            roc_curve_data = {}
            roc_auc_scores = {}
            for model_name in model_names_list:
                model_pred_y = self.sklearn_components["test_set_predictions"][
                    model_name
                ]
                fpr, tpr, thresholds = sklearn.metrics.roc_curve(
                    y_true=self.data["y_test_for_model"],
                    y_score=model_pred_y,
                )
                roc_curve_data[model_name] = {
                    "fpr": fpr,
                    "tpr": tpr,
                    "thresholds": thresholds,
                }
                roc_auc_scores[model_name] = sklearn.metrics.roc_auc_score(
                    y_true=self.data["y_test_for_model"], y_score=model_pred_y
                )
            roc_auc_scores = dict(
                sorted(roc_auc_scores.items(), key=lambda item: item[1], reverse=True)
            )

            print(
                """--ROC AUC Scores (test data)--
The "ROC AUC Score" is the area under the ROC Curve
It is also the probability that a random positive (y=1) case and a random negative (y=0) case are ranked correctly by the model 
            """
            )
            for model_name in roc_auc_scores:
                print(f"\t{model_name}: {roc_auc_scores[model_name]:.2f}")

            plt.figure(figsize=(10, 7))
            for model_name in roc_curve_data:
                plt.plot(
                    roc_curve_data[model_name]["fpr"],
                    roc_curve_data[model_name]["tpr"],
                    label=model_name,
                )
            plt.axline([0, 0], [1, 1])
            plt.legend()
            plt.title("ROC Curves (Test Data)")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate (Recall)")
            [plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
            [plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
            plt.show()

    def compare_models_calibration_test_set(
        self, model_names_list: List[str], n_bins: int = 5
    ) -> None:
        """Plots a Calibration Curve for each model (on the same plot) using their test data predictions

        Parameters
        ----------
        model_names_list: List[str]
            The models to include in the plot (list of model names)
            Note that the model name format must match the format of the model names given previously in the define_models() function
        n_bins: int, optional (default=5)
            The number of bins to use when constructing the calibration curves
        """
        model_calibration_explanation_text = r"""
-- Model Calibration --
A well-calibrated classifier is one whose predictions are directly interpretable as probabilities
    e.g. 44% of samples with predicted outcome Pr[Y=1]=0.44 are observed to have outcome y=1  
This can be assessed using a "Calbration Curve", which is constructed as follows:
    * The samples are ordered by model predicted outcome Pr[Y=1]
    * The samples are binned (typically equal-sized bins)
    * Average (mean) model predicted outcome Pr[Y=1] is plotted against observed proportion of postive (y=1) cases for each bin
A model with perfect calibration has a "Calibration Curve" which is an upward 45 degree straight line
A binary classifier model with poor calibration can still be very useful (e.g. it can still rank order samples well)
The importance of model calibration depends upon the use case
        """
        code_str = f"""
# compare models performance on test data: calibration curves #        
\"\"\"
{model_calibration_explanation_text}
\"\"\"
calibration_curve_data = {{}}
model_names_list = {model_names_list}
for model_name in model_names_list:
    calib_p_true, calib_p_pred = sklearn.calibration.calibration_curve(
        y_true=y_test_for_model,
        y_prob=test_data_predictions[model_name],
        n_bins={n_bins},
    )
    calibration_curve_data[model_name] = {{
        "p_true": calib_p_true,
        "p_pred": calib_p_pred,
    }}

plt.figure(figsize=(10, 7))
for model_name in calibration_curve_data:
    plt.plot(
        calibration_curve_data[model_name]["p_pred"],
        calibration_curve_data[model_name]["p_true"],
        label=model_name,
    )
plt.axline([0, 0], [1, 1], color="black", linestyle="dotted")
plt.legend()
plt.title("Calibration Curves (Test Data)")
plt.xlabel("Mean Predicted Pr[Y=1]")
plt.ylabel("Observed y=1 Proportion")
[plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
[plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
plt.show()
"""
        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            print(model_calibration_explanation_text)

            calibration_curve_data = {}
            for model_name in model_names_list:
                calib_p_true, calib_p_pred = sklearn.calibration.calibration_curve(
                    y_true=self.data["y_test_for_model"],
                    y_prob=self.sklearn_components["test_set_predictions"][model_name],
                    n_bins=n_bins,
                )
                calibration_curve_data[model_name] = {
                    "p_true": calib_p_true,
                    "p_pred": calib_p_pred,
                }

            plt.figure(figsize=(10, 7))
            for model_name in calibration_curve_data:
                plt.plot(
                    calibration_curve_data[model_name]["p_pred"],
                    calibration_curve_data[model_name]["p_true"],
                    label=model_name,
                )
            plt.axline([0, 0], [1, 1], color="black", linestyle="dotted")
            plt.legend()
            plt.title("Calibration Curves (Test Data)")
            plt.xlabel("Mean Predicted Pr[Y=1]")
            plt.ylabel("Observed y=1 Proportion")
            [plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
            [plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
            plt.show()

    def compare_models_test_set_precision_recall(
        self, model_names_list: List[str]
    ) -> None:
        """Plots a "Precision vs Recall Curve" for each model (on the same plot) using their predictions on the test data

        Parameters
        ----------
        model_names_list: List[str]
            The models to include in the plot (list of model names)
            Note that the model name format must match the format of the model names given previously in the define_models() function
        """
        precision_recall_explanation_text = """
-- Model Precision vs Recall --
   "Recall" = The proportion of true positive (y=1) cases which the model has correctly labelled as positive (y=1)
"Precision" = The proportion of predicted positive (y=1) cases which are truly positive (y=1) cases
        
The Precision/Recall Curve (for a single model) plots the Precision and Recall achieved under a range of different "decision thresholds" (between 0.0 and 1.0)
For a given "decision threshold", all samples with estimated Pr[y=1] higher than that threshold are labelled as the positive (y=1) class

With decreasing threshold, recall is monotonically increasing.
Perhaps surprisingly, precision is not necessarily monotonically decreasing with decreasing threshold value.
        """

        code_str = f"""
# compare models performance on test data: precision vs recall #        
\"\"\"
{precision_recall_explanation_text}
\"\"\"
precision_recall_curve_data = {{}}
model_names_list = {model_names_list}
for model_name in model_names_list:
    model_pred_y = test_data_predictions[model_name]
    precision, recall, thresholds = sklearn.metrics.precision_recall_curve(
        y_true=y_test_for_model,
        probas_pred=model_pred_y,
    )
    precision_recall_curve_data[model_name] = {{
        "precision": precision,
        "recall": recall,
        "thresholds": thresholds,
    }}
plt.figure(figsize=(10, 7))
for model_name in precision_recall_curve_data:
    plt.plot(
        precision_recall_curve_data[model_name]["recall"],
        precision_recall_curve_data[model_name]["precision"],
        label=model_name,
    )
plt.legend()
plt.title("Precision vs Recall Curves (Test Data)")
plt.xlabel("Recall")
plt.ylabel("Precision")
[plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
[plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
plt.show()        
        """

        self.full_model_script += code_str

        if self.global_params["verbose"]:
            print(code_str)

        if self.global_params["eval_code"]:
            print(precision_recall_explanation_text)
            precision_recall_curve_data = {}
            for model_name in model_names_list:
                model_pred_y = self.sklearn_components["test_set_predictions"][
                    model_name
                ]
                precision, recall, thresholds = sklearn.metrics.precision_recall_curve(
                    y_true=self.data["y_test_for_model"],
                    probas_pred=model_pred_y,
                )
                precision_recall_curve_data[model_name] = {
                    "precision": precision,
                    "recall": recall,
                    "thresholds": thresholds,
                }
            plt.figure(figsize=(10, 7))
            for model_name in precision_recall_curve_data:
                plt.plot(
                    precision_recall_curve_data[model_name]["recall"],
                    precision_recall_curve_data[model_name]["precision"],
                    label=model_name,
                )
            plt.legend()
            plt.title("Precision Recall Curves (Test Data)")
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            [plt.axhline(x / 10, alpha=0.2) for x in range(0, 10)]
            [plt.axvline(x / 10, alpha=0.2) for x in range(0, 10)]
            plt.show()


if __name__ == "__main__":
    # run example #
    data_df = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
        header=None,
        names=[
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
            "annual_salary",
        ],
    ).sample(1_000)
    data_df["annual_salary_over_50k"] = (data_df["annual_salary"] == " >50K").astype(
        int
    )
    sk_classifier = RapidBinaryClassifier(data_df=data_df, verbose=True, eval_code=True)
    sk_classifier.assess_input_data_quality()
    sk_classifier.set_variable_roles_in_model(
        y_varname="annual_salary_over_50k",
        x_numeric_varnames=[
            "age",
            "fnlwgt",
            "education-num",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
        ],
        x_categorical_varnames=[
            "workclass",
            "education",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native-country",
        ],
    )
    sk_classifier.generate_train_test_split(test_percent=0.2)
    sk_classifier.transform_x_features(rare_category_min_freq=500)
    sk_classifier.define_models(
        {
            "adaboost": sklearn.ensemble.AdaBoostClassifier(),
            "decision_tree": sklearn.tree.DecisionTreeClassifier(),
            "extremely_random_trees": sklearn.ensemble.ExtraTreesClassifier(),
            "gaussian_naive_bayes": sklearn.naive_bayes.GaussianNB(),
            # "gaussian_process": sklearn.gaussian_process.GaussianProcessClassifier(),
            "hist_gbm": sklearn.ensemble.HistGradientBoostingClassifier(),
            "logistic_regression": sklearn.linear_model.LogisticRegression(
                penalty=None,
                max_iter=1_000,
            ),
            "neural_net": sklearn.neural_network.MLPClassifier(
                hidden_layer_sizes=(50, 30, 10, 5), activation="relu", max_iter=1_000
            ),
            "quadratic_discriminant_analysis": sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis(),
            "random_forest": sklearn.ensemble.RandomForestClassifier(),
        }
    )
    all_model_names = list(sk_classifier.sklearn_components["models"].keys())
    sk_classifier.fit_cross_valid_models(
        k_folds=10,
        model_names_list=all_model_names,
    )
    sk_classifier.compare_models_cross_valid_roc_auc()
    sk_classifier.add_ensemble_model(
        ensemble_name="weighted_avg_ensemble_all_models",
        model_names_list=all_model_names,
        combine_strategy="weighted_average",
    )
    sk_classifier.add_ensemble_model(
        ensemble_name="weighted_avg_ensemble_best_models",
        model_names_list=[
            "adaboost",
            "hist_gbm",
            "logistic_regression",
            "random_forest",
        ],
        combine_strategy="weighted_average",
    )
    sk_classifier.add_ensemble_model(
        ensemble_name="stacked_classifier_ensemble_all_models",
        model_names_list=all_model_names,
        combine_strategy="stacked_classifier",
        meta_model=sklearn.ensemble.HistGradientBoostingClassifier(),
    )
    sk_classifier.fit_cross_valid_models(
        k_folds=10,
        model_names_list=[
            "weighted_avg_ensemble_all_models",
            "weighted_avg_ensemble_best_models",
            "stacked_classifier_ensemble_all_models",
        ],
    )
    sk_classifier.compare_models_cross_valid_roc_auc()
    final_chosen_model_names_list = [
        "adaboost",
        "hist_gbm",
        "logistic_regression",
        "weighted_avg_ensemble_best_models",
        "stacked_classifier_ensemble_all_models",
    ]
    sk_classifier.fit_models(model_names_list=final_chosen_model_names_list)
    sk_classifier.generate_test_set_predictions(
        model_names_list=final_chosen_model_names_list
    )
    sk_classifier.compare_models_test_set_roc_curves(
        model_names_list=final_chosen_model_names_list
    )
    sk_classifier.compare_models_calibration_test_set(
        model_names_list=final_chosen_model_names_list, n_bins=10
    )
    sk_classifier.compare_models_test_set_precision_recall(
        model_names_list=final_chosen_model_names_list
    )
