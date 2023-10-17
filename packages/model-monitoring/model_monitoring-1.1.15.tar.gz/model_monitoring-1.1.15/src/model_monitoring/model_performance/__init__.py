import pandas as pd
import numpy as np
from typing import Dict
import warnings

from model_monitoring.utils import check_metrics_sets

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold = params["performance_threshold"]


class PerformancesDrift:
    """Performance Drift Class."""

    def __init__(self, perf_metrics_curr, config_threshold=None):
        """Performance Drift Class.

        Args:
            perf_metrics_curr (dict): dictionary containing current metrics perfomances
            config_threshold (dict, optional): dictionary containing threshold settings. Defaults to None.
        """
        if not isinstance(perf_metrics_curr, Dict):
            raise ValueError(
                "Performance metrics in input has not a valid format. It should be a dictionary containing functions as keys and values as values."
            )
        if config_threshold is None:
            config_threshold = standard_threshold

        check_metrics = [i for i in perf_metrics_curr.keys() if i not in config_threshold.keys()]
        if len(check_metrics) > 0:
            warnings.warn(f"{check_metrics} do not have threshold settings in config_threshold")

        list_com_metrics = list(set(perf_metrics_curr.keys()).intersection(set(config_threshold.keys())))

        # initialize report
        report_df = (
            pd.DataFrame.from_dict({x: perf_metrics_curr[x] for x in list_com_metrics}, "index", columns=["curr_perf"])
            .reset_index()
            .rename(columns={"index": "metric"})
        )
        self.report = report_df

        self.perf_metrics_curr = perf_metrics_curr
        self.config_threshold = config_threshold
        self.perf_metrics_stor = None

    def get_absolute(self):
        """Load on the report the absolute alert on current metrics perfomances."""
        # Generation Alert
        for a in self.report.metric.values:
            absolute_red = self.config_threshold[a]["absolute"]["red"]
            absolute_yellow = self.config_threshold[a]["absolute"]["yellow"]
            curr_perf = self.report.loc[self.report.metric == a, "curr_perf"].values[0]
            if self.config_threshold[a]["logic"] == "decrease":
                if absolute_red != "None":
                    if curr_perf < absolute_red:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = "Red Alert"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf > absolute_red) and (curr_perf < absolute_yellow):
                                self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                else:
                    if absolute_yellow != "None":
                        if curr_perf < absolute_yellow:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
            elif self.config_threshold[a]["logic"] == "increase":
                if absolute_red != "None":
                    if curr_perf > absolute_red:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = "Red Alert"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf < absolute_red) and (curr_perf > absolute_yellow):
                                self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                else:
                    if absolute_yellow != "None":
                        if curr_perf > absolute_yellow:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )
        # Locate Absolute_warning after Curr_perf
        absolute_warning = self.report.pop("absolute_warning")
        self.report.insert(2, "absolute_warning", absolute_warning)

    def get_relative(self, perf_metrics_stor):
        """Load on the report the historichal metrics performances, drift compared to the current performances and relative alert on drift.

        Args:
            perf_metrics_stor (dict): dictionary containing historichal metrics perfomances.
        """
        # Check if the metrics are the same
        check_metrics_sets(metrics_1=perf_metrics_stor, metrics_2=self.perf_metrics_curr)

        list_com_metrics = list(set(perf_metrics_stor.keys()).intersection(set(self.perf_metrics_curr.keys())))
        self.perf_metrics_stor = {x: perf_metrics_stor[x] for x in list_com_metrics}
        stor_perf_df = (
            pd.DataFrame.from_dict(self.perf_metrics_stor, "index", columns=["stor_perf"])
            .reset_index()
            .rename(columns={"index": "metric"})
        )
        try:
            self.report.loc[:, "stor_perf"] = stor_perf_df.stor_perf
        except Exception:
            self.report = self.report.merge(stor_perf_df, how="outer", on="metric")

        # Generation Drift
        for a in self.report.metric.values:
            stor_perf = self.report.loc[self.report.metric == a, "stor_perf"].values[0]
            curr_perf = self.report.loc[self.report.metric == a, "curr_perf"].values[0]
            if self.config_threshold[a]["logic"] in ["decrease", "increase"]:
                if stor_perf > 0:
                    self.report.loc[self.report.metric == a, "drift_perc"] = (curr_perf - stor_perf) / stor_perf * 100
                else:
                    self.report.loc[self.report.metric == a, "drift_perc"] = (stor_perf - curr_perf) / stor_perf * 100
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )

        # Generation Alert
        for a in self.report.metric.values:
            relative_red = self.config_threshold[a]["relative"]["red"]
            relative_yellow = self.config_threshold[a]["relative"]["yellow"]
            drift_perf = self.report.loc[self.report.metric == a, "drift_perc"].values[0]
            if self.config_threshold[a]["logic"] == "decrease":
                if relative_red != "None":
                    if drift_perf < relative_red * 100:
                        self.report.loc[self.report.metric == a, "relative_warning"] = "Red Alert"
                    else:
                        if relative_yellow != "None":
                            if (drift_perf > relative_red * 100) and (drift_perf < relative_yellow * 100):
                                self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                else:
                    if relative_yellow != "None":
                        if drift_perf < relative_yellow * 100:
                            self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
            elif self.config_threshold[a]["logic"] == "increase":
                if relative_red != "None":
                    if drift_perf > relative_red * 100:
                        self.report.loc[self.report.metric == a, "relative_warning"] = "Red Alert"
                    else:
                        if relative_yellow != "None":
                            if (drift_perf < relative_red * 100) and (drift_perf > relative_yellow * 100):
                                self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                else:
                    if relative_yellow != "None":
                        if drift_perf > relative_yellow * 100:
                            self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )

    def get_report(self):
        """Return the report.

        Returns:
            pd.DataFrame: report of the class.
        """
        return self.report
