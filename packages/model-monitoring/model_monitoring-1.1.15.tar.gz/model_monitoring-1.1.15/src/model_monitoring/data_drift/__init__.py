import pandas as pd
from typing import Dict

from model_monitoring.data_drift.data_drift import psi_report
from model_monitoring.utils import check_features_sets, convert_Int_dataframe

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold_psi = params["data_drift_threshold"]


class DataDrift:
    """Data Drift Class."""

    def __init__(self, data_stor, data_curr, type_data="auto", feat_to_check=None, config_threshold=None):
        """Data Drift Class.

        Args:
            data_stor (pd.DataFrame/dict): historical dataset.
            data_curr (pd.DataFrame/dict): current dataset.
            type_data (str, optional): indicates the type of input data among "data" (pd.DataFrame), "metadata" (dict of metadata containing for each feature the bin mapping) and "auto".
                If "data" is provided as input the class computes data drift on orginal data, while for "metadata" input it computes data drift on information contained in dictionaries.
                Defaults to "auto".
            feat_to_check (list, optional): list of features to be checked. Deafualts to None.
            config_threshold (dict, optional): dictionary containing psi threshold settings. Defaults to None.
        """
        # Set psi threshold
        if config_threshold is None:
            config_threshold = standard_threshold_psi
        self.config_threshold = config_threshold

        if type_data not in ["auto", "data", "metadata"]:
            raise ValueError(
                f"{type_data} is not a valid type_data. It should be one of the following:\n ['auto','data','metadata']"
            )

        if type_data == "auto":
            if isinstance(data_stor, pd.DataFrame) and isinstance(data_curr, pd.DataFrame):
                type_data = "data"
            elif isinstance(data_stor, Dict) and isinstance(data_stor, Dict):
                type_data = "metadata"
            else:
                raise ValueError("format data inputs are not valid. Choose both pd.DataFrame or both dict")
        self.type_data = type_data

        if type_data == "data":
            check_features_sets(features_1=list(data_stor.columns), features_2=list(data_curr.columns))
            list_com_features = list(set(data_stor.columns).intersection(set(data_curr.columns)))
        else:
            check_features_sets(features_1=list(data_stor.keys()), features_2=list(data_curr.keys()))
            list_com_features = list(set(data_stor.keys()).intersection(set(data_curr.keys())))
        if len(list_com_features) == 0:
            raise ValueError("No features in common between the two sets")

        if feat_to_check is None:
            feat_to_check = list_com_features

        self.feat_to_check = feat_to_check

        self.data_stor_original = data_stor
        self.data_curr_original = data_curr
        if type_data == "data":
            self.data_stor = convert_Int_dataframe(data_stor[self.feat_to_check])
            self.data_curr = convert_Int_dataframe(data_curr[self.feat_to_check])
        else:
            self.data_stor = {x: data_stor[x] for x in self.feat_to_check}
            self.data_curr = {x: data_curr[x] for x in self.feat_to_check}

        # Check valid format for metadata
        if type_data == "metadata":
            for x in self.feat_to_check:
                if "type" not in self.data_stor[x].keys():
                    raise ValueError(f"not type provided for {x} feature in reference metadata")
                elif "type" not in self.data_curr[x].keys():
                    raise ValueError(f"not type provided for {x} feature in new metadata")
                else:
                    if self.data_stor[x]["type"] not in ["categorical", "numerical"]:
                        raise ValueError(
                            f"{self.data_stor[x]['type']} not valid type for {x} feature. Choose among ['categorical','numerical']"
                        )
                    if self.data_curr[x]["type"] not in ["categorical", "numerical"]:
                        raise ValueError(
                            f"{self.data_curr[x]['type']} not valid type for {x} feature. Choose among ['categorical','numerical']"
                        )
                    if self.data_stor[x]["type"] == "numerical":
                        if "min_val" not in self.data_stor[x].keys():
                            raise ValueError(f"not min_val provided for {x} numerical feature in reference metadata")
                        if "max_val" not in self.data_stor[x].keys():
                            raise ValueError(f"not max_val provided for {x} numerical feature in reference metadata")
                        for y in [
                            k
                            for k in self.data_stor[x].keys()
                            if k not in ["type", "min_val", "max_val", "missing_values"]
                        ]:
                            if "min" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not min provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                            if "max" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not max provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                            if "freq" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                    if self.data_curr[x]["type"] == "numerical":
                        if "min_val" not in self.data_curr[x].keys():
                            raise ValueError(f"not min_val provided for {x} numerical feature in new metadata")
                        if "max_val" not in self.data_curr[x].keys():
                            raise ValueError(f"not max_val provided for {x} numerical feature in new metadata")
                        for y in [
                            k
                            for k in self.data_curr[x].keys()
                            if k not in ["type", "min_val", "max_val", "missing_values"]
                        ]:
                            if "min" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not min provided for {x} numerical feature for {y} bin in new metadata"
                                )
                            if "max" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not max provided for {x} numerical feature for {y} bin in new metadata"
                                )
                            if "freq" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} numerical feature for {y} bin in new metadata"
                                )
                    if self.data_stor[x]["type"] == "categorical":
                        for y in [k for k in self.data_stor[x].keys() if k not in ["type", "missing_values"]]:
                            if "labels" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not labels provided for {x} categorical feature for {y} bin in reference metadata"
                                )
                            if "freq" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} categorical feature for {y} bin in reference metadata"
                                )
                    if self.data_curr[x]["type"] == "categorical":
                        for y in [k for k in self.data_curr[x].keys() if k not in ["type", "missing_values"]]:
                            if "labels" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not labels provided for {x} categorical feature for {y} bin in new metadata"
                                )
                            if "freq" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} categorical feature for {y} bin in new metadata"
                                )

        # Initialize the report
        self.data_drift_report = None
        self.meta_ref_dict = None

    def report_drift(self, psi_nbins=1000, psi_bin_min_pct=0.04, drift_missing=True, return_meta_ref=False):
        """Retrieve the report with psis for each feature in both dataframe sets and `Warning` alerts if the psis exceed thresholds.

        Args:
            psi_nbins (int, optional): number of bins into which the features will be bucketed (maximum) to compute psi. Defaults to 1000.
            psi_bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.
            drift_missing (bool, optional): boolean to add to the report information on missing values drift. Defaults to False.
            return_meta_ref (bool, optional): boolean to save as attribute of the class the reference metadata dictionary. Defaults to False.

        Returns:
            pd.DataFrame: report of the class.
        """
        self.psi_nbins = psi_nbins
        self.psi_bin_min_pct = psi_bin_min_pct
        self.drift_missing = drift_missing
        self.return_meta_ref = return_meta_ref

        # data drift psi report
        data_drift_report, meta_ref_dict = psi_report(
            base_df=self.data_stor,
            compare_df=self.data_curr,
            type_data=self.type_data,
            feat_to_check=self.feat_to_check,
            max_psi=self.config_threshold["max_psi"],
            mid_psi=self.config_threshold["mid_psi"],
            psi_nbins=self.psi_nbins,
            psi_bin_min_pct=self.psi_bin_min_pct,
            return_meta_ref=self.return_meta_ref,
        )
        self.meta_ref_dict = meta_ref_dict

        # missing values drift
        if drift_missing:
            if self.type_data == "data":
                perc_drift_missing = pd.Series(
                    (
                        self.data_curr[self.feat_to_check].isnull().mean()
                        - self.data_stor[self.feat_to_check].isnull().mean()
                    )
                    * 100,
                    name="drift_perc_missing",
                )
                if self.return_meta_ref:
                    for col in self.meta_ref_dict:
                        self.meta_ref_dict[col]["missing_values"] = self.data_stor[col].isnull().mean()
            else:
                missing_dict = dict()
                for col in self.feat_to_check:
                    try:
                        missing_dict[col] = (
                            self.data_curr[col]["missing_values"] - self.data_stor[col]["missing_values"]
                        ) * 100
                    except Exception:
                        raise ValueError(f"no missing values provided for {col} feature")
                perc_drift_missing = pd.DataFrame.from_dict(
                    missing_dict, orient="index", columns=["drift_perc_missing"]
                )
            data_drift_report = data_drift_report.merge(perc_drift_missing, left_on="feature", right_index=True)
        self.data_drift_report = data_drift_report
        return self.data_drift_report

    def get_meta_ref(self):
        """Return the reference metadata dictionary.

        Returns:
            dict: reference metadata dictionary.
        """
        return self.meta_ref_dict
