from tqdm import tqdm
import sys

from model_monitoring.utils import (
    get_categorical_features,
    get_numerical_features,
    check_features_sets,
    convert_Int_dataframe,
)
from model_monitoring.reference_metadata.reference_metadata import retrieve_bins_dict, map_bins_dict


class ReferenceMetaData:
    """Reference Meta-Data Class."""

    def __init__(self, meta_ref_dict=None):
        """Reference Meta-Data Class.

        Args:
            meta_dict (dict, optional): reference metadata dictionary. Defaults to None.
        """
        self.meta_ref_dict = meta_ref_dict

    def get_meta_reference(self, data_reference, feat_to_check=None, nbins=1000, bin_min_pct=0.04, missing_values=True):
        """Retrieve the reference metadata dictionary.

        Args:
            data_reference (pd.DataFrame): original dataset for generating the reference metadata dictionary. Defaults to None.
            feat_to_check (list, optional): list of features to be checked. Deafualts to None.
            nbins (int, optional): number of bins into which the features will be bucketed (maximum). Defaults to 1000.
            bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.
            missing_values (bool, optional): boolean to add to the metadata dictionary information on missing values. Defaults to True.

        Returns:
            dict: reference metadata dictionary
        """
        if feat_to_check is None:
            feat_to_check = data_reference.columns

        self.feat_to_check = feat_to_check
        self.data_reference = convert_Int_dataframe(data_reference)

        self.nbins = nbins
        self.bin_min_pct = bin_min_pct
        self.missing_values = missing_values

        # Generation reference metadata dictionary
        meta_ref_dict = dict()
        numerical_feat = get_numerical_features(self.data_reference[self.feat_to_check])
        categorical_feat = get_categorical_features(self.data_reference[self.feat_to_check])

        features_pb = tqdm(self.feat_to_check, file=sys.stdout, desc="Performing bin mapping", ncols=100, leave=True)
        for ix, col in enumerate(features_pb):
            col_dict = dict()
            if col in numerical_feat:
                col_dict["type"] = "numerical"
                col_dict["min_val"] = self.data_reference[col].min()
                col_dict["max_val"] = self.data_reference[col].max()
            if col in categorical_feat:
                col_dict["type"] = "categorical"
            bins_dict = retrieve_bins_dict(self.data_reference, col, nbins=self.nbins, bin_min_pct=self.bin_min_pct)[
                col
            ]
            if bins_dict != dict():
                col_dict.update(bins_dict)
            if missing_values:
                col_dict["missing_values"] = self.data_reference[col].isnull().mean()
            meta_ref_dict[col] = col_dict

            if ix == len(self.feat_to_check) - 1:
                features_pb.set_description("Completed bin mapping", refresh=True)

        self.meta_ref_dict = meta_ref_dict

        return self.meta_ref_dict

    def get_meta_new(self, new_data, meta_dict=None):
        """Retrieve the metadata dictionary for new data using the reference metadata dictionary.

        Args:
            new_data (pd.DataFrame): new dataset.
            meta_dict (dict, optional): reference metadata dictionary. Defaults to None.

        Returns:
            dict: metadata dictionary for new data
        """
        if (meta_dict is None) and (self.meta_ref_dict is None):
            raise ValueError("no reference metadata dictionary provided")
        elif meta_dict is None:
            meta_dict = self.meta_ref_dict
        # Check if the features are the same
        check_features_sets(features_1=list(meta_dict.keys()), features_2=list(new_data.columns))

        list_com_metrics = list(set(meta_dict.keys()).intersection(set(new_data.columns)))
        self.new_data = convert_Int_dataframe(new_data[list_com_metrics])
        self.meta_dict = {k: meta_dict[k] for k in list_com_metrics}

        # Generation metadata dictionary for new data
        meta_new_dict = dict()
        for col in list_com_metrics:
            col_dict = dict()
            if self.meta_dict[col]["type"] not in ["categorical", "numerical"]:
                raise ValueError(
                    f"{self.meta_dict[col]['type']} is not a valid type for {col} feature. Choose between ['categorical','numerical']."
                )
            else:
                col_dict["type"] = self.meta_dict[col]["type"]
            if col_dict["type"] == "numerical":
                col_dict["min_val"] = self.new_data[col].min()
                col_dict["max_val"] = self.new_data[col].max()
            bins_dict = map_bins_dict(self.new_data, self.meta_dict, col)[col]
            if bins_dict != dict():
                col_dict.update(bins_dict)
            if "missing_values" in self.meta_dict[col]:
                col_dict["missing_values"] = self.new_data[col].isnull().mean()
            meta_new_dict[col] = col_dict

        self.meta_new_dict = meta_new_dict

        return self.meta_new_dict
