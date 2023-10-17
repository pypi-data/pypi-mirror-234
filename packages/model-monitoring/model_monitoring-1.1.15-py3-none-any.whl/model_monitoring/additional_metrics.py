import pandas as pd
import numpy as np
from sklearn.metrics import recall_score


def lift_score(y_true, y_prob, method: str = "percentile", percentile: float = 0.2, threshold: float = 0.5):
    """Calculates the lift score which compares the model true positive rate versus a random choice.

    Args:
        y_true (np.array, pd.Series): real value of target
        y_prob (np.array, pd.Series): predicted probability of the target
        method (str, optional): 'percentile' or 'threshold'. If percentile it uses the defined percentiles to set the cutoff.
            If threshold it uses the defined threshold as cutoff. Default percentile
        percentile (float, optional): Percentile to use to get the cutoff. Defaults to 0.2.
        threshold (float, optional): Threshold to use as cutoff. Defaults to 0.5.

    Returns:
        float: lift score
    """
    checker_te = pd.DataFrame({"events": y_true, "prob": y_prob})
    if method == "percentile":
        cutoff = checker_te.prob.quantile(q=1 - percentile)
    else:
        cutoff = threshold
    if checker_te["events"].sum() == 0:
        raise ValueError("y_true always 0")

    tpr_db = checker_te.loc[checker_te.prob > cutoff]
    tpr_model = tpr_db["events"].sum() / tpr_db.shape[0]
    tpr_random = checker_te["events"].sum() / checker_te.shape[0]

    return tpr_model / tpr_random


def gain_score(y_true, y_prob, method: str = "percentile", percentile: float = 0.2, threshold: float = 0.5):
    """Calculates the gain score which identifies the recall at a cutoff.

    Args:
        y_true (np.array, pd.Series): real value of target
        y_prob (np.array, pd.Series): predicted probability of the target
        method (str, optional): 'percentile' or 'threshold'. If percentile it uses the defined percentiles to set the cutoff.
            If threshold it uses the defined threshold as cutoff. Default percentile
        percentile (float, optional): Percentile to use to get the cutoff. Defaults to 0.2.
        threshold (float, optional): Threshold to use as cutoff. Defaults to 0.5.

    Returns:
        float: gain score
    """
    checker_te = pd.DataFrame({"events": y_true, "prob": y_prob})
    if method == "percentile":
        cutoff = checker_te.prob.quantile(q=1 - percentile)
    else:
        cutoff = threshold
    if checker_te["events"].sum() == 0:
        raise ValueError("y_true always 0")
    return recall_score(y_true, np.where(checker_te.prob > cutoff, 1, 0))
