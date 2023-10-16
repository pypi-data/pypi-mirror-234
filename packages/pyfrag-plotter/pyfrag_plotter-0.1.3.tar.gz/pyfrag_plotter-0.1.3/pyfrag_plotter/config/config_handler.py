""" Module that contains the functions for initializing the config file and reading the config file. This module should be imported by any module that needs to read the config file. """
from __future__ import annotations
import re
import configparser as cp
from typing import Dict, Callable, Any, List
from pyfrag_plotter.config.validate import validate_config_key
from pyfrag_plotter.errors import PyFragConfigValidationError


def _get_str_key(config_parser: cp.ConfigParser, section: str, option: str) -> str:
    value = config_parser.get(section, option)
    return value.strip()


def _get_list_str_key(config_parser: cp.ConfigParser, section: str, option: str) -> List[str]:
    # Split the value string using a regular expression that matches any whitespace character
    value = re.split(r'\s*,\s*|\s+', config_parser.get(section, option))
    return [v for v in value if v]


def _get_float_key(config_parser: cp.ConfigParser, section: str, option: str) -> float:
    value = config_parser.getfloat(section, option)
    return value


def _get_list_float_key(config_parser: cp.ConfigParser, section: str, option: str) -> List[float]:
    value = re.split(r'\s*,\s*|\s+', config_parser.get(section, option))
    value = [float(v.strip()) for v in value]
    return value


def _get_int_key(config_parser: cp.ConfigParser, section: str, option: str) -> int:
    value = config_parser.getint(section, option)
    return value


def _get_boolean_key(config_parser: cp.ConfigParser, section: str, option: str) -> bool:
    value = config_parser.getboolean(section, option)
    return value


def _get_any_key(config_parser: cp.ConfigParser, section: str, option: str) -> Any:
    # First, try to get the value as an integer
    try:
        value = config_parser.getint(section, option)
    except ValueError:
        # If that fails, try to get the value as a float
        try:
            value = config_parser.getfloat(section, option)
        except Exception:
            # If that fails, get the value as a string
            value = config_parser.get(section, option)
            value = value.strip()
    return value


config_key_to_function_mapping: Dict[str, Callable[..., Any]] = {
    # Shared keys
    "log_level": _get_str_key,
    "x_lim": _get_list_float_key,
    "y_lim": _get_list_float_key,
    "colours": _get_list_str_key,
    "line_styles": _get_list_str_key,
    "outlier_threshold": _get_float_key,
    "trim_option": _get_any_key,
    "vline": _get_float_key,
    "trim_key": _get_str_key,
    "reverse_x_axis": _get_boolean_key,
    "stat_point_type": _get_str_key,
    "n_interpolation_points": _get_int_key,

    # EDA keys
    "eda_keys": _get_list_str_key,

    # ASM keys
    "asm_keys": _get_list_str_key,
    "asm_strain_keys": _get_list_str_key,

    # Matplotlib keys
    "fig_size": _get_list_float_key,
    "font": _get_str_key,
    "font_size": _get_int_key,
}


class Config:
    """An interface for the config file.

    This class overloads the get method of the ConfigParser class to ensure that the correct type is returned.

    Attributes:
        config_parser (ConfigParser): The ConfigParser instance that contains the configuration data.

    """

    def __init__(self, config_parser) -> None:
        self.config_parser: cp.ConfigParser = config_parser

    def get(self, section: str, option: str) -> Any:
        """Gets the value of the specified option in the specified section.

        This method returns the value with the correct type.

        Args:
            section (str): The name of the section that contains the option.
            option (str): The name of the option to get.

        Returns:
            ret_variable (Any): The value of the specified option in the specified section.

        Raises:
            ValueError: If the specified option is not a valid option.
            ValueError: If the specified section is not a valid section.

        """
        option = option.lower()
        if option not in config_key_to_function_mapping:
            raise ValueError(f"Option '{option}' is not a valid option. Valid options are {list(config_key_to_function_mapping.keys())}.\nPlease check the config file.")

        if section not in self.config_parser:
            raise ValueError(f"Section '{section}' is not a valid section. Valid sections are {self.sections}.")

        ret_variable = config_key_to_function_mapping[option](self.config_parser, section, option)
        return ret_variable

    @property
    def sections(self) -> List[str]:
        """Gets a list of the sections in the config file.

        Returns:
            List[str]: A list of the sections in the config file.

        """
        return self.config_parser.sections()

    @property
    def content(self) -> Dict[str, Dict[str, Any]]:
        """Gets a dictionary containing the content of the config file.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary containing the content of the config file.

        """
        return {section: dict(self.config_parser[section]) for section in self.config_parser.sections()}

    def overwrite_config(self, config_parser: cp.ConfigParser):
        """ Overwrites the current config parser with a new config parser. This is used to overwrite the default config parser with a user-specified config parser with the |init| function."""
        self.config_parser = config_parser

    def validate_config(self):
        """ Validates all available config keys. It checks whether:
            - the user specified keys are valid keys (valid keys are specified in the config_key_to_function_mapping dictionary)
            - the user specified keys have the correct values

        Raises:
            PyFragConfigValidationError (PyFragConfigValidationError): If the config key is invalid.

        Note: it uses the |validate| function from the validate module.
        """
        # First checks whether all required keys are present
        config_keys = [key for key in self.config_parser.defaults().keys()]
        if not all([key in config_keys for key in config_key_to_function_mapping.keys()]):
            raise PyFragConfigValidationError(f"Not all required keys are present in the config file. Please check if these keys are specified {list(config_key_to_function_mapping.keys())}.")

        # Then check every key-value pair
        for section, config_keys in self.content.items():
            for config_key in config_keys:
                typed_value_of_config_key = config_key_to_function_mapping[config_key](self.config_parser, section, config_key)
                validate_config_key(config_key, typed_value_of_config_key, list(config_key_to_function_mapping.keys()))
