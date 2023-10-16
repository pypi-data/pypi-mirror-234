import inspect
import math
from typing import Callable, Optional, Tuple, Sequence

import matplotlib.figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MaxNLocator

from pyfrag_plotter import config
from pyfrag_plotter.interpolate import interpolate_plot


def replace_overlapping_keys(func: Callable) -> Callable:
    """A decorator that replaces overlapping keys between kwargs and function arguments with top-level input.

    This decorator is used to ensure that the correct input is used for a function when both positional arguments and keyword arguments are used.
    It replaces overlapping keys between kwargs and function arguments with top-level input.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.

    """
    argspec = inspect.getfullargspec(func)
    kwargs_only = argspec.kwonlyargs

    def wrapper(*args, **kwargs):
        # First get the valid keys (i.e. keys that are also function arguments)
        valid_kwargs = kwargs.copy()
        for key in kwargs:
            if key not in argspec.args:
                valid_kwargs.pop(key)

        # Then, find overlapping keys between the valid keys from the kwargs and function arguments
        overlapping_keys = set(valid_kwargs) & set(list(args) + kwargs_only)

        # Replace overlapping keys with top-level input
        for key in overlapping_keys:
            valid_kwargs[key] = argspec.annotations.get(key, type(valid_kwargs[key]))(valid_kwargs[key])

        return func(*args, **valid_kwargs)

    return wrapper


@replace_overlapping_keys
def set_figure_details(
    fig: Optional[matplotlib.figure.Figure] = None,
    title: Optional[str] = None,
    savefig: Optional[str] = None,
    show_plot: bool = False,
    clear_plot: bool = False,
    tight_layout: bool = True,
) -> None:
    """Specifies figure options for making a shorter and cleaner code.

    Args:
        fig (Optional[matplotlib.figure.Figure], optional): The figure to modify. Defaults to None.
        title (Optional[str], optional): The title of the figure. Defaults to None.
        savefig (Optional[str], optional): The filename to save the figure to. Defaults to None.
        show_plot (bool, optional): Whether to show the plot. Defaults to False.
        clear_plot (bool, optional): Whether to clear the plot. Defaults to False.
        tight_layout (bool, optional): Whether to use tight layout. Defaults to True.
    """
    fig = plt.gcf() if fig is None else fig

    # Fixes the large padding between the axes and the labels of the axes
    if tight_layout:
        fig.tight_layout()

    # Adds a title to the figure
    if title is not None:
        fig.suptitle(title, fontweight='bold', y=1.00)

    # Saves the figure in standard .png format.
    if savefig is not None:
        fig.savefig(savefig, dpi=600)

    if show_plot:
        plt.show()

    if clear_plot:
        plt.clf()


@replace_overlapping_keys
def set_axes_details(
    ax: Optional[plt.Axes] = None,
    x_label: str = "\u0394r / \u00c5",
    y_label: str = "\u0394$\it{E}$ / kcal mol$^{-1}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    y_lim: Optional[Tuple[float, float]] = None,
    n_max_x_ticks: int = 6,
    n_max_y_ticks: int = 5,
    plot_legend: bool = True,
    line_style_labels: Optional[Sequence[str]] = None,
) -> None:
    """Specifies axes options for making a shorter and cleaner code.

    Args:
        ax (Optional[plt.Axes], optional): The axes to modify. Defaults to None.
        x_label (str, optional): The label for the x-axis. Defaults to "\u0394r / \u00c5" (dr / A).
        y_label (str, optional): The label for the y-axis. Defaults to "\u0394$\it{E}$ / kcal mol$^{-1}$" (dE / kcal mol-1).
        y_lim (Optional[Tuple[float, float]], optional): The y-axis limits. Defaults to None.
        n_max_x_ticks (int, optional): The maximum number of x-axis ticks. Defaults to 6.
        n_max_y_ticks (int, optional): The maximum number of y-axis ticks. Defaults to 5.
        plot_legend (bool, optional): Whether to plot the legend. Defaults to True.
        line_style_labels (Optional[Sequence[str]], optional): The legend for the line styles. Defaults to None.
    """
    ax = plt.gca() if ax is None else ax

    # Plot labels
    ax.set_xlabel(x_label, labelpad=20)
    ax.set_ylabel(y_label, labelpad=20)

    # Specfies the y limits
    if y_lim is None:
        default_y_lim = config.get("SHARED", "y_lim")
        ax.set_ylim(default_y_lim[0], default_y_lim[1])
    else:
        ax.set_ylim(y_lim[0], y_lim[1])

    # Plot x limits
    x_lim = config.get("SHARED", "x_lim")
    ax.set_xlim(x_lim[0], x_lim[1])

    # Reverses the plot direction by reversing the x-axis
    reverse_x_axis = config.get("SHARED", "reverse_x_axis")
    if reverse_x_axis:
        ax.set_xlim(ax.get_xlim()[::-1][0], ax.get_xlim()[1])

    # Smoothens the plots in the specified range (x_lim) by interpolating the data using the scipy spline library
    for line in ax.lines:
        x, y = line.get_data()
        X_, Y_ = interpolate_plot(x, y)
        line.set_data(X_, Y_)

    # Draws a vertical line at the specified point
    # First check for user input, else check for config file input
    vline = config.get("SHARED", "vline")
    if not math.isclose(vline, 0.0):
        ax.vlines(
            vline,
            ax.get_ylim()[0],
            ax.get_ylim()[1],
            colors=["grey"],
            linestyles="dashed",
        )

    # Draws a horizontal line at y=0 (indicating the 'zero line')
    ax.hlines(0, ax.get_xlim()[0], ax.get_xlim()[1], colors=["grey"], linewidth=0.2)

    # Set the y-axis formatter to round to one decimal place
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # Axes adjustments: tick markers and number of ticks
    ax.tick_params(which="both", width=1.5)
    ax.tick_params(which="major", length=7)
    ax.xaxis.set_major_locator(MaxNLocator(n_max_x_ticks))
    ax.yaxis.set_major_locator(MaxNLocator(n_max_y_ticks))

    # Removes the top en right border of the graph
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Makes the x and y axis wider
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)

    # Adds more spacing between ticks and the labels
    ax.tick_params(pad=6)

    # Plots the legend below the title showing the system names
    if plot_legend:
        system_name_legend = ax.legend(frameon=False)
        ax.add_artist(system_name_legend)

        # Plots another legend for multiple linestyles for the same system
        # It gets the lines and overwrites the labels with the line_style_labels
        if line_style_labels is not None:
            lines = ax.lines
            n_systems = len(lines) // len(line_style_labels)
            lines = [ax.lines[i] for i in range(0, len(lines), n_systems)]

            # Overwrite the labels
            [line.set_label(label) for line, label in zip(lines, line_style_labels)]
            second_legend = ax.legend(
                handles=lines,
                loc="upper center",
                ncol=len(line_style_labels)//2 if len(line_style_labels) > 2 else 1,
                frameon=False,
            )
            ax.add_artist(second_legend)
