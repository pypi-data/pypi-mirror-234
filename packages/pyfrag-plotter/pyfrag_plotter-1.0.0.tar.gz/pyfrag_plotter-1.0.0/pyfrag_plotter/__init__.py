from pyfrag_plotter.config.config_handler import Config
import os
import configparser as cp
from typing import Optional
import logging


# Global variable that contains the config file. It is first empty, but will be filled in the |init| function
config: Config = Config(cp.ConfigParser())


def initialize_pyfrag_plotter(user_config_file: Optional[str] = None) -> None:
    """Initializes the PyFrag plotter configuration.

    Reads the standard configuration file provided in the module and sets the config as global variable that is read throughout the program.
    May be overwritten by providing a custom configuration file.

    Args:
        user_config_file (Optional[str]): The path to a custom configuration file. Defaults to None.

    Returns:
        None

    """
    global config

    # Get the absolute path of the directory one level above the current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Construct the path to the configuration file
    config_file = os.path.join(current_dir, 'config', 'config.ini')

    # Read the default config file
    config_parser = cp.ConfigParser()
    config_parser.read(config_file)

    # Read the user config file if provided and overwrite the config file
    if user_config_file is not None:
        config_parser.read(user_config_file)

    # Finally, check if all config keys are valid
    # This it to make it easier for providing user-friendly error messages
    config.overwrite_config(config_parser)
    config.validate_config()

    # Initialize the log level and plot parameters
    logging.basicConfig(level=config.get("SHARED", "log_level"))
    _initialize_plot_parameters()


def _initialize_plot_parameters() -> None:
    """Applies plot-specific parameters to matplotlib and is called by :func:`pyfrag_plotter.initialize_pyfrag_plotter`.

    This function sets various parameters for matplotlib, such as the figure size, font family, and font size.

    """
    import matplotlib as mpl

    # In some occations matplotlib cannot use the interactive backend, so we try to use the non-interactive backend
    try:
        mpl.use("TkAgg")
        import matplotlib.pyplot as plt
    except ImportError:
        mpl.use("Agg")
        import matplotlib.pyplot as plt

    # Get a list of available fonts of matplotlib
    # import matplotlib.font_manager
    # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # print(names)

    # mp.font_manager._rebuild()
    # font = fp.FontProperties(fname=r"C:\\Windows\\Fonts\\Helvetica Regulier.ttf")
    # print(font.get_name())

    # Figure size
    plt.rcParams["figure.figsize"] = config.get("MATPLOTLIB", "fig_size")

    # Font family
    plt.rcParams["font.family"] = config.get("MATPLOTLIB", "font")

    # Takes care of ticks starting at the edge of the screen
    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["axes.xmargin"] = 0.00
    plt.rcParams["axes.ymargin"] = 0.00

    font_size = config.get("MATPLOTLIB", "font_size")

    plt.rc("font", size=font_size)  # controls default text sizes
    plt.rc("axes", titlesize=font_size)  # fontsize of the axes title
    plt.rc("axes", labelsize=font_size)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=font_size - 2)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=font_size - 2)  # fontsize of the tick labels
    plt.rc("legend", fontsize=font_size - 7)  # legend fontsize
    plt.rc("figure", titlesize=font_size + 2)  # fontsize of the figure title
