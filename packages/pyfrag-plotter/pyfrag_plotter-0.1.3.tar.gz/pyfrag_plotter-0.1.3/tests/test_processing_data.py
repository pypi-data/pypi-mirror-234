import pandas as pd
import pytest
from pyfrag_plotter.processing_funcs import _trim_data_float, _trim_data_int, _trim_data_str, remove_dispersion_term, remove_outliers, remove_duplicate_x_values_dataframe

OUTLIER_THRESHOLD = 50


@pytest.fixture
def regular_df():
    return pd.DataFrame({
        "EnergyTotal": [
            0.40939,
            9.56754,
            15.22111,
            17.08688,
            19.07092,
            21.03672,
            22.79637,
            24.08829,
            23.96248,
            13.28778,
            0.34548,
            -6.09441,
            -22.56811,
            -33.61639,
            -36.88992,
            -37.21977]
    }
    )


@pytest.fixture
def df_with_outliers():
    return pd.DataFrame({
        "EnergyTotal": [
            0.40939,
            9.56754,
            15.22111,
            17.08688,
            160.07092,
            100.03672,
            40.79637,
            24.08829,
            23.96248,
            13.28778,
            0.34548,
            -6.09441,
            -100.56811,
            -160.61639,
            -36.88992,
            -37.21977]
    }
    )


def test_trim_data_float(regular_df):
    result = _trim_data_float(regular_df, 10.0, "EnergyTotal")
    assert len(result) == 2
    assert result["EnergyTotal"].max() <= 10.0


def test_trim_data_int(regular_df):
    result = _trim_data_int(regular_df, 3, "EnergyTotal")
    assert len(result) == 3


def test_trim_data_str_min(regular_df):
    result = _trim_data_str(regular_df, "min", "EnergyTotal")
    assert len(result) == 16


def test_trim_data_str_max(regular_df):
    result = _trim_data_str(regular_df, "max", "EnergyTotal")
    assert len(result) == 8
    assert result["EnergyTotal"].iloc[-1] == result["EnergyTotal"].max()


def test_remove_dispersion_term_with_dispersion():
    # Test the function with a dataframe that has a non-zero dispersion term
    df = pd.DataFrame({
        "Energy": [-10.0, -20.0, -30.0],
        "Disp": [0.1, 0.2, 0.3]
    })
    expected_df = df.copy()
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_without_dispersion():
    # Test the function with a dataframe that has a zero dispersion term
    df = pd.DataFrame({
        "Energy": [-10.0, -20.0, -30.0],
        "Disp": [0.0, 0.0, 0.0]
    })
    expected_df = df.drop(columns=["Disp"])
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_with_empty_dataframe():
    # Test the function with an empty dataframe
    df = pd.DataFrame()
    expected_df = pd.DataFrame()
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_with_single_row_dataframe():
    # Test the function with a dataframe that has a single row
    df = pd.DataFrame({
        "Energy": [-10.0],
        "Disp": [0.0]
    })
    expected_df = df.drop(columns=["Disp"])
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_outliers_values(df_with_outliers):
    # Check that the outliers have been removed
    expected = pd.DataFrame({
        "EnergyTotal": [
            0.40939,
            9.56754,
            15.22111,
            17.08688,
            40.79637,
            24.08829,
            23.96248,
            13.28778,
            0.34548,
            -6.09441,
            -36.88992,
            -37.21977]
    }
    )
    result = remove_outliers(df_with_outliers, OUTLIER_THRESHOLD)["EnergyTotal"]
    expected = expected["EnergyTotal"].reset_index(drop=True)
    result = result.reset_index(drop=True)
    # Not checking the index type because the index type of the expected and result Series are different
    pd.testing.assert_series_equal(result, expected)


def test_remove_outliers_length(df_with_outliers):
    # Check that the length of the resulting DataFrame is correct
    expected_length = len(df_with_outliers) - 4
    result_length = len(remove_outliers(df_with_outliers, OUTLIER_THRESHOLD))
    assert result_length == expected_length


def test_remove_duplicate_x_values_dataframe_no_duplicates():
    # Test the function with a DataFrame that has no duplicates
    df = pd.DataFrame({
        "bondlength_1": [1, 2, 3],
        "energy": [10, 20, 30]
    })
    expected_df = df.copy()
    assert remove_duplicate_x_values_dataframe(df).equals(expected_df)


def test_remove_duplicate_x_values_dataframe_with_duplicates():
    # Test the function with a DataFrame that has duplicates
    df = pd.DataFrame({
        "bondlength_1": [1, 2, 2, 3],
        "energy": [10, 20, 25, 30]
    })
    expected_df = pd.DataFrame({
        "bondlength_1": [1, 2, 3],
        "energy": [10, 25, 30]
    })
    assert remove_duplicate_x_values_dataframe(df).equals(expected_df)


def test_remove_duplicate_x_values_dataframe_multiple_x_axes():
    # Test the function with a DataFrame that has multiple x-axis columns
    df = pd.DataFrame({
        "bondlength_1": [1, 2, 2, 3],
        "angle_1": [10, 20, 25, 30],
        "energy": [100, 200, 250, 300]
    })
    expected_df = pd.DataFrame({
        "bondlength_1": [1, 2, 3],
        "angle_1": [10, 25, 30],
        "energy": [100, 250, 300]
    })
    assert remove_duplicate_x_values_dataframe(df).equals(expected_df)


def test_remove_duplicate_x_values_dataframe_empty_dataframe():
    # Test the function with an empty DataFrame
    df = pd.DataFrame()
    expected_df = pd.DataFrame()
    assert remove_duplicate_x_values_dataframe(df).equals(expected_df)


def test_remove_duplicate_x_values_dataframe_single_row_dataframe():
    # Test the function with a DataFrame that has a single row
    df = pd.DataFrame({
        "bondlength_1": [1],
        "energy": [10]
    })
    expected_df = df.copy()
    assert remove_duplicate_x_values_dataframe(df).equals(expected_df)
