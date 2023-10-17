""" Module for validating the inputs of the config file """
from typing import Dict, Any, Sequence, Union, List
from pyfrag_plotter.errors import PyFragConfigValidationError


ALLOWED_VALUES: Dict[str, Sequence[Any]] = {
    "log_level": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "trim_option": ["min", "max", "x_lim", "false"],
    "reverse_x_axis": ["false", "true"],
    "stat_point_type": ["min", "max", "none"],
    "eda_keys": ["Int", "Pauli", "Elstat", "OI", "Disp"],
    "asm_keys": ["EnergyTotal", "StrainTotal", "Int"],
    "asm_strain_keys": ["StrainTotal", "frag1Strain", "frag2Strain"]
}


def _check_if_key_is_valid_key(key: str, validation_keys: Sequence[str]) -> None:
    """ Validates whether the user-speicifkey is a valid key """
    if key not in validation_keys:
        raise PyFragConfigValidationError(f"Key '{key}' is not present in the config file. Please check the config file.", key=key)


def _check_if_key_has_allowed_value(key: Union[List, str], value: Any) -> None:
    """ Validates whether the user has specified an appropriate value in config file """

    # Check if the key is present in the ALLOWED_VALUES dictionary.
    # Other keys are not validated because they are not as sensitive to specific values such as x_lim being a list of floats
    if key not in ALLOWED_VALUES:
        return

    # If the key is present, check if the value is in the list of allowed values
    allowed_values_for_key = ALLOWED_VALUES[key]

    # For strings, check if the value is in the list of allowed values
    if isinstance(value, str):
        if value not in allowed_values_for_key:
            raise PyFragConfigValidationError(f"Key '{key}' has value '{value}'. This value is not allowed. Allowed values are: {', '.join(ALLOWED_VALUES[key])}.", key=key)

    # For lists, check if all values are in the list of allowed values.
    # Example is the eda_keys key, which is a list of strings
    elif isinstance(value, Sequence):
        for val in value:
            if val not in allowed_values_for_key:
                raise PyFragConfigValidationError(f"Key '{key}' has value '{val}'. This value is not allowed. Allowed values are: {', '.join(ALLOWED_VALUES[key])}.", key=key)


def _change_formats_of_specific_keys(config_keys: Dict[str, Any]) -> None:
    """ Changes the key format of specific keys to the correct format.

    For example, "line_styles" can be str values, but it could also be a tuple of int values. This function changes the format of the key to the correct format."""
    raise NotImplementedError


def validate_config_key(key: str, value: Any, validation_keys: Sequence[str]) -> None:
    """
    Validates a configuration key-value pair against a list of valid keys.

    Args:
        key (str): The key to validate.
        value (Any): The value to validate.
        validation_keys (Sequence[str]): A list of valid keys.

    Returns:
        None
    """
    # Because the configparser keys are case-insensitive, we need to make sure that the keys are all lowercase
    key = key.lower()
    validation_keys = [validation_key.lower() for validation_key in validation_keys]

    # Check if all required keys are present
    _check_if_key_is_valid_key(key, validation_keys)

    # Check if all keys have the appropriate value
    _check_if_key_has_allowed_value(key, value)
