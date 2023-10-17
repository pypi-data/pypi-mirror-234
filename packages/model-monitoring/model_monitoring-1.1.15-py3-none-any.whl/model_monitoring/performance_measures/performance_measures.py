def compute_metric(y_true, y_pred, metric, **kwargs):
    """Compute the supervised metric scoring.

    Args:
        y_true (pd.Series/np.array): true values of target
        y_pred (pd.Series/np.array): predictions/scores of target
        metric (function): metric function

    Returns:
        metric scoring performance
    """
    return metric(y_true, y_pred, **kwargs)
