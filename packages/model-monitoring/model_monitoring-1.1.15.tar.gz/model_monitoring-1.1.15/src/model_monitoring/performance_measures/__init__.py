# regression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    explained_variance_score,
    median_absolute_error,
)

# classification
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
)

import warnings
import pandas as pd
import numpy as np
from typing import Dict

from model_monitoring.utils import check_size, convert_Int_series
from model_monitoring.performance_measures.performance_measures import compute_metric


class PerformancesMeasures:
    """Performance Measures Class."""

    def __init__(self, model_type="auto", set_metrics="standard", new_metrics=None, **kwargs):
        """Performance Measures Class.

        Args:
            model_type (str): Modelling problem among "regression", "classification", "multiclass" and "auto".
            set_metrics (str, optional): Metrics settings. It can be set "standard" for classical ML metrics, "new" for setting a new dictionary of metrics and "add" for adding new metrics to the standard ones. Defaults to 'standard'.
            new_metrics (dict, optional): Dictionary of new metrics as keys when "set_metrics" is set to "new" and "add", and one among ['pred','prob'] as values. Defaults to None.
        """
        # Check the model_type
        if model_type not in ["auto", "regression", "classification", "multiclass"]:
            raise ValueError(
                f"{model_type} is not a valid algo_type. It should be one of the following:\n ['auto', 'regression', 'classification', 'multiclass']"
            )
        else:
            self.model_type = model_type

        # Check the set_metrics
        if set_metrics not in ["standard", "add", "new"]:
            raise ValueError(
                f"{set_metrics} is not a valid set_metrics. It should be one of the following:\n ['standard', 'add', 'new']"
            )
        self.set_metrics = set_metrics

        # Check new_metrics
        if self.set_metrics in ["add", "new"]:
            if new_metrics is None:
                self.new_metrics = {}
            else:
                if isinstance(new_metrics, Dict):
                    if set(new_metrics.values()).issubset(set(["pred", "prob"])):
                        self.new_metrics = new_metrics
                    else:
                        raise ValueError(
                            f"{list(set(new_metrics.values()))} contains invalid input. Valid inputs are ['pred', 'prob']"
                        )
                else:
                    raise ValueError(
                        f"{new_metrics} has not a valid format. It should be a dictionary containing functions as keys and one of ['pred', 'prob'] as values."
                    )

        # Set the metrics for each set_metric case
        if self.set_metrics == "new":
            self.metrics = self.new_metrics
        if self.set_metrics in ["standard", "add"]:
            if self.model_type == "regression":
                self.metrics = {
                    mean_squared_error: "pred",
                    r2_score: "pred",
                    median_absolute_error: "pred",
                    explained_variance_score: "pred",
                }
            elif self.model_type == "classification":
                self.metrics = {
                    balanced_accuracy_score: "pred",
                    accuracy_score: "pred",
                    precision_score: "pred",
                    recall_score: "pred",
                    f1_score: "pred",
                    roc_auc_score: "prob",
                }
            else:
                self.metrics = {balanced_accuracy_score: "pred", accuracy_score: "pred", roc_auc_score: "prob"}
            if self.set_metrics == "add":
                self.metrics = {**self.metrics, **self.new_metrics}

        self.predictions = None
        self.prob = None
        self.target = None
        self.perf_metrics = None
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def compute_metrics(self, target, predictions=None, prob=None, **kwargs):
        """Compute metrics performances.

        Args:
            target (np.array/pd.Series): target column
            predictions (np.array/pd.Series, optional): Predictions array. Defaults to None.
            prob (np.array/pd.Series, optional): Probabilities prob for classification. Defaults to None.

        Returns:
            dict: metrics performances
        """
        for k, v in kwargs.items():
            self.__dict__[k] = v

        # Check one among predictions and prob exists
        if (predictions is None) and (prob is None):
            raise ValueError("at least one among predictions and prob must be not None")

        # Check size of the predictions and target
        if predictions is not None:
            check_size(predictions, target)

        # Check size of the target and prob
        if prob is not None:
            check_size(target, prob)

        if isinstance(target, np.ndarray):
            target = pd.Series(target, name="target")
        vals = target.nunique()
        if vals == 1:
            raise ValueError(f"The target column {target} selected is constant")
        elif self.model_type == "auto":
            if vals == 2:
                self.model_type = "classification"
            elif vals < 11:
                self.model_type = "multiclass"
            else:
                self.model_type = "regression"

        if self.model_type == "regression":
            if predictions is None:
                raise ValueError("predictions not provided")

        self.target = convert_Int_series(target)
        if predictions is not None:
            self.predictions = convert_Int_series(predictions)
        else:
            self.predictions = predictions
        if prob is not None:
            self.prob = convert_Int_series(prob)
        else:
            self.prob = prob

        perf_metrics = dict()
        if self.model_type == "regression":
            for i, j in self.metrics.items():
                dict_to_use = {k: v for k, v in self.__dict__.items() if k in i.__code__.co_varnames}
                if j == "pred":
                    perf_metrics[i.__name__] = compute_metric(self.target, self.predictions, metric=i, **dict_to_use)
                else:
                    warnings.warn(f"{j} is a wrong label for regression model type. Label {i.__name__} with 'pred'.")
        elif self.model_type == "classification":
            if self.predictions is None:
                try:
                    self.predictions = self.prob.apply(lambda x: 1 if x > 0.5 else 0)
                except Exception:
                    self.predictions = np.array([1 if i > 0.5 else 0 for i in self.prob])
            for i, j in self.metrics.items():
                dict_to_use = {k: v for k, v in self.__dict__.items() if k in i.__code__.co_varnames}
                if j == "prob":
                    if self.prob is None:
                        warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                    else:
                        perf_metrics[i.__name__] = compute_metric(self.target, self.prob, metric=i, **dict_to_use)
                else:
                    perf_metrics[i.__name__] = compute_metric(self.target, self.predictions, metric=i, **dict_to_use)
        elif self.model_type == "multiclass":
            if self.predictions is None:
                self.predictions = pd.Series([np.argmax(x) for x in self.prob], name="prob")
            for i, j in self.metrics.items():
                dict_to_use = {k: v for k, v in self.__dict__.items() if k in i.__code__.co_varnames}
                if i.__name__ in [
                    "precision_score",
                    "recall_score",
                    "f1_score",
                    "fbeta_score",
                    "brier_score_loss",
                    "class_likelihood_ratios",
                    "dcg_score",
                    "jaccard_score",
                    "log_loss",
                    "matthews_corrcoef",
                    "ndcg_score",
                ]:
                    warnings.warn(f"{i.__name__} is used for binary classification")
                elif j == "prob":
                    if self.prob is None:
                        warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                    else:
                        perf_metrics[i.__name__] = compute_metric(self.target, self.prob, metric=i, multi_class="ovr")
                else:
                    perf_metrics[i.__name__] = compute_metric(self.target, self.predictions, metric=i, **dict_to_use)
        else:
            raise ValueError("Invalid model type.")

        self.perf_metrics = perf_metrics
        return self.perf_metrics
