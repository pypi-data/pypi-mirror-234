import math
from typing import Any, Callable, Dict, Optional, Sequence, Union
import numpy as np
import pandas as pd

from pyfrag_plotter import config
from pyfrag_plotter.errors import PyFragResultsProcessingError, PyFragResultsProcessingWarning

# ====================================================================================================
# Main Processing Function   =========================================================================
# ====================================================================================================


def process_results_file(
        df: pd.DataFrame,
        trim_option: Optional[Union[str, float, int, Sequence]] = None,
        trim_key: Optional[str] = None,
        outlier_threshold: Optional[float] = None,
) -> pd.DataFrame:
    """Processes the results file data.

    Args:
        df: A pandas DataFrame containing the results file data.
        trim_option: An optional argument specifying how to trim the data. Can be "max", "min", "x_limits", or None.
        trim_key: An optional argument specifying the key to use for trimming the data. Can be "EnergyTotal" or None.
        outlier_threshold: An optional argument specifying the threshold for removing outliers. Can be a float or None.

    Returns:
        A pandas DataFrame containing the processed results file data.

    Raises:
        PyFragResultsProcessingError: If an error occurs during processing.

    """
    # Trim the data
    df = trim_data(df, trim_option, trim_key)

    # Remove duplicate x values
    df = remove_duplicate_x_values_dataframe(df)

    # Remove the dispersion term if it is 0.0 everywhere
    df = remove_dispersion_term(df)

    # Remove outliers
    df = remove_outliers(df, outlier_threshold)

    return df

# ====================================================================================================
# Data Trimming   ====================================================================================
# ====================================================================================================


def _trim_data_str(df: pd.DataFrame, trim_option: str, trim_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a string trim_option"""
    trim_option = trim_option.lower().strip()

    if trim_option in ["false", "none"]:
        return df

    if trim_option == "max":
        max_index = df[trim_key].idxmax()
        df = df.loc[:max_index]
    elif trim_option == "min":
        min_index = df[trim_key].idxmin()
        df = df.loc[:min_index]

    return df


def _trim_data_float(df: pd.DataFrame, trim_option: float, trim_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a float trim_option"""
    index = (df[trim_key] - trim_option).abs().idxmin()
    df = df.loc[:index]
    return df


def _trim_data_int(df: pd.DataFrame, trim_option: int, trim_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a integer trim_option"""
    df = df.iloc[:trim_option]
    return df


def _trim_data_sequence(df: pd.DataFrame, trim_option: Sequence[float], trim_key: str) -> pd.DataFrame:
    """ Private function that performs the actual trimming of the dataframe with a sequence trim_option"""

    x_limits = trim_option
    reverse_axis = bool(config.get("SHARED", "reverse_x_axis"))

    if not (trim_key.startswith("bondlength_") or trim_key.startswith("angle_") or trim_key.startswith("dihedral_")):
        PyFragResultsProcessingWarning(section="_trim_data_sequence",
                                       message=f"trim_key {trim_key} is not valid. Valid options are bondlength_x, angle_x, and dihedral_x. Proceeding with bondlength_1.")
        trim_key = "bondlength_1"

    if not isinstance(x_limits, Sequence) or len(x_limits) != 2 or x_limits[0] >= x_limits[1]:
        raise PyFragResultsProcessingError(key="trim_data_sequence", message=f"Invalid x_limits {x_limits} specified in the configuration file.")

    x_data: np.ndarray = df[trim_key].values  # type: ignore since it is a numpy array
    x_min = max(x_data.min(), x_limits[0])
    x_max = min(x_data.max(), x_limits[1])
    x_indices = np.where((x_data >= x_min) & (x_data <= x_max))[0]
    if x_indices.size == 0:
        raise PyFragResultsProcessingError(key="trim_data_sequence", message=f"No data points within the specified x limits {x_limits} for key {trim_key}.")

    if not reverse_axis:
        x_indices = np.concatenate(([max(0, x_indices[0] - 1)], x_indices, [min(x_data.size - 1, x_indices[-1] + 1)]))
    else:
        x_indices = np.concatenate(([max(0, x_indices[0] + 1)], x_indices, [min(x_data.size - 1, x_indices[-1] - 1)]))

    df = df.iloc[x_indices]
    return df


_overload_types: Dict[Any, Callable[..., pd.DataFrame]] = {
    str: _trim_data_str,
    float: _trim_data_float,
    int: _trim_data_int,
    Sequence: _trim_data_sequence,
}


def trim_data(df: pd.DataFrame, trim_option: Optional[Union[str, float, int, Sequence]] = None, trim_key: Optional[str] = None) -> pd.DataFrame:
    """'Overloaded' function to trim the dataframe based on the type of the trim_option.

    This function trims the given dataframe based on the type of the trim_option.
    The trim_option is read from the configuration file and can be either a string ("min", "max"), integer (IRC point), float (energy value), or a sequence (x_limits such as (1.0, 3.0))).
    The function returns the trimmed dataframe.

    Args:
        df (pd.DataFrame): The dataframe to trim.
        trim_parameter (Optional[Union[str, float, int]]): The parameter to use for trimming. Defaults to None.
        trim_key (Optional[str]): The key to use for reading the trim_parameter from the configuration file. Defaults to None.

    Raises:
        PyFragResultsProcessingError: If the trim_option is not a valid type.

    Returns:
        pd.DataFrame: The trimmed dataframe.

    """
    trim_key = config.get("SHARED", "trim_key") if trim_key is None else trim_key
    trim_option = config.get("SHARED", "trim_option") if trim_option is None else trim_option

    # Sometimes, users might specify a trim_key in the config file that is not in the dataframe
    if trim_key not in df.columns:
        raise PyFragResultsProcessingError(key="trim_data", message=f"trim_key {trim_key} is not a valid key. Check if 'trim_key' in the config file is correct.")

    # Check if the trim_option is a valid type such as a string, float, or integer
    if not isinstance(trim_option, (str, float, int, Sequence)):
        raise PyFragResultsProcessingError(key="trim_data", message=f"trim_option {trim_option} is not a valid type. Valid types are str, float, and int")

    # Handle the case where the trim_option is a string but needs to be converted to a sequence (i.e. x_lim)
    if isinstance(trim_option, str):
        trim_option = trim_option.lower().strip()
        if trim_option in ["x_lim", "xlim", "x_limits", "xlimits"]:
            trim_option = tuple(config.get("SHARED", "x_lim"))

    for key, value in _overload_types.items():
        if isinstance(trim_option, key):
            return value(df, trim_option, trim_key)

    return df


# ====================================================================================================
# Dispersion term check ==============================================================================
# ====================================================================================================

def remove_dispersion_term(df: pd.DataFrame) -> pd.DataFrame:
    """Removes the dispersion term from the dataframe if it is 0.0 everywhere.

    This function takes a pandas DataFrame containing the results file data and removes the dispersion term if it is 0.0 everywhere. The function returns the modified DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the results file data.

    Returns:
        pd.DataFrame: The modified DataFrame without the dispersion term if it is 0.0 everywhere.

    """
    if "Disp" not in df.columns:
        return df

    # Check if the dispersion term is 0.0 everywhere
    if all([math.isclose(value, 0.0) for value in df["Disp"]]):
        # Remove the dispersion term
        df = df.drop(columns=["Disp"])

    return df


# ====================================================================================================
# Removing Outliers ==================================================================================
# ====================================================================================================

def remove_outliers(df: pd.DataFrame, outlier_threshold: Optional[float] = None) -> pd.DataFrame:
    """Removes outliers from the dataframe.

    This function takes a pandas DataFrame containing the results file data and removes outliers from the dataframe. The function returns the modified DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the results file data.

    Returns:
        pd.DataFrame: The modified DataFrame without outliers.

    """
    outlier_threshold = config.get("SHARED", "outlier_threshold") if outlier_threshold is None else outlier_threshold

    # Calculate the difference between each value and its two nearest neighbors from both ends
    diff = df["EnergyTotal"].diff().abs()
    diff_forward = df["EnergyTotal"].diff(periods=2).abs()
    diff_backward = df["EnergyTotal"].iloc[::-1].diff(periods=2).abs().iloc[::-1]

    # Identify the outliers
    outliers = (diff > outlier_threshold) & (diff_forward > outlier_threshold) & (diff_backward > outlier_threshold)

    # Remove the outliers
    df = df[~outliers]

    return df

# ====================================================================================================
# Removing duplicate x values ========================================================================
# ====================================================================================================


def remove_duplicate_x_values_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with duplicate x-axis values from a pandas DataFrame. This is necessary since otherwise the interpolation will fail.

    Args:
        df (pd.DataFrame): The DataFrame to remove duplicates from.
        x_axis_key (str): The name of the column containing the x-axis values.
        y_axis_key (str): The name of the column containing the y-axis values.

    Returns:
        pd.DataFrame: The modified DataFrame with duplicates removed.
    """

    x_axis_keys = [key for key in df.columns if key.startswith("bondlength_") or key.startswith("angle_") or key.startswith("dihedral_")]

    # Remove duplicate rows
    for x_axis_key in x_axis_keys:
        df = df.drop_duplicates(subset=x_axis_key, keep="last")

    # Reset the index of the DataFrame
    df = df.reset_index(drop=True)

    # Return the modified DataFrame
    return df
