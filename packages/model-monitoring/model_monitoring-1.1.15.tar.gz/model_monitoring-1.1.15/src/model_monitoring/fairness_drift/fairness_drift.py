import pandas as pd
import numpy as np
from functools import reduce
import warnings


def fair_from_dict(fair_dict, label=["curr_perf", "curr_perc_label"]):
    """Generates a Multiindex Dataframe starting from current fairness metrics dictionary.

    Args:
        fair_dict (dict): dictionary containing current fairness metrics performance
        label (list, optional): label names of column at level 2 in the Multiindex DataFrame. Deafaults to ["curr_perf","curr_perc_label"].

    Returns:
        pd.DataFrame: Multiindex Dataframe
    """
    reformed_total = dict()
    for a in fair_dict.keys():
        reformed_dict = dict()
        for outerKey, innerDict in fair_dict[a].items():
            for innerKey, values in innerDict.items():
                for i in range(len(label)):
                    reformed_dict[(outerKey, innerKey, label[i])] = values[i]
        reformed_total[a] = reformed_dict

    return pd.DataFrame.from_dict(reformed_total, orient="index").reset_index().rename(columns={"index": "metric"})


def add_absolute_alert_columns(report_df, absolute=False):
    """Add empty columns of Absolute warning for each label (or group of labels) for each feature (or group of features) to the Multiindex Report of FairnessDrift Class.

    Args:
        report_df (pd.DataFrame): Multiindex report of the FairnessDrift Class.
        absolute (bool, optional): it indicates if the columns on absolute warning have been already added. Defaults to False.

    Returns:
        pd.DataFrame: Multiindex DataFrame with Absolute warning columns added
    """
    if not absolute:
        old_dict = report_df.to_dict()
        new_dict = {("metric", "", ""): old_dict[("metric", "", "")]}
        for x in [y for y in old_dict.keys() if y != ("metric", "", "")]:
            new_dict[x] = old_dict[x]
            if x[2] == "curr_perc_label":
                new_dict[(x[0], x[1], "absolute_warning")] = {k: np.nan for k in old_dict[x].keys()}
        return pd.DataFrame(new_dict)
    else:
        return report_df


def add_relative_alert_columns(report_df):
    """Add empty columns of Relative warning and drift for each label (or group of labels) for each feature (or group of features) to the Multiindex Report of FairnessDrift Class.

    Args:
        report_df (pd.DataFrame): Multiindex report of the FairnessDrift Class.

    Returns:
        pd.DataFrame: Multiindex DataFrame with Relative warning and drift columns added
    """
    old_dict = report_df.to_dict()
    new_dict = {("metric", "", ""): old_dict[("metric", "", "")]}
    for x in [y for y in old_dict.keys() if y != ("metric", "", "")]:
        new_dict[x] = old_dict[x]
        if x[2] == "stor_perc_label":
            new_dict[(x[0], x[1], "drift_perc")] = {k: np.nan for k in old_dict[x].keys()}
            new_dict[(x[0], x[1], "relative_warning")] = {k: np.nan for k in old_dict[x].keys()}

    return pd.DataFrame(new_dict)


def check_fairness_groups(df_1, df_2, multiindex=True):
    """Check if two DataFrames have different group of fairness or if Multiindex Dataframes have different columns until level 1 and retrieves the list of unmatched fairness groups.

    Args:
        df_1 (pd.DataFrame): Multiindex DataFrame 1
        df_2 (pd.DataFrame): Multiindex DataFrame 2
        multiindex (bool, optional): determines if args are Multiindex Dataframes or DataFrames. Default to True.

    Returns:
        list: list of unmatched fairness groups unmatched.
    """
    if multiindex:
        col_2_train = reduce(
            lambda l, y: l.append(y) or l if y not in l else l, [(x[0], x[1]) for x in df_1.columns], []
        )
        col_2_test = reduce(
            lambda l, y: l.append(y) or l if y not in l else l, [(x[0], x[1]) for x in df_2.columns], []
        )
        list_no_join = list(set(col_2_train) ^ set(col_2_test))
    else:
        list_no_join = list(set(df_1.groups) ^ set(df_2.groups))
    if len(list_no_join) != 0:
        warnings.warn(f"unmatched fairness groups {list_no_join}")

    return list_no_join


def bg_red_yellow(df):
    """Color report of Class Fairness Drift based on Alert.

    Args:
        df (pd.DataFrame): report in input

    Returns:
        pd.DataFrame: color-mapping report
    """
    ret = pd.DataFrame("", index=df.index, columns=df.columns)
    for x in np.unique([x for x in df.columns.levels[0] if x != "metric"]):
        for y in np.unique(df[x].columns.get_level_values(0)):
            if "absolute_warning" in df[x][y].columns:
                ret.loc[
                    df[x][y].absolute_warning == "Red Alert", [(x, y, "curr_perf"), (x, y, "absolute_warning")]
                ] = "background-color: red"
                ret.loc[
                    df[x][y].absolute_warning == "Yellow Alert", [(x, y, "curr_perf"), (x, y, "absolute_warning")]
                ] = "background-color: yellow"

            ret.loc[
                df[x][y].relative_warning == "Red Alert", [(x, y, "drift_perc"), (x, y, "relative_warning")]
            ] = "background-color: red"
            ret.loc[
                df[x][y].relative_warning == "Yellow Alert", [(x, y, "drift_perc"), (x, y, "relative_warning")]
            ] = "background-color: yellow"
    return ret
