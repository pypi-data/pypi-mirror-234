"""Visplotlib pyplot module."""
import os
import warnings

import matplotlib.pyplot as plt

from .dims import GOLDEN_SLIDE, set_dim

filepath = os.path.dirname(os.path.abspath(__file__))

# Use Visium styling
plt.style.use(filepath + "/visium.mplstyle")


VISIUM_LIGHT = "#5eb2fc"
VISIUM_CLASSIC = "#0858cf"
VISIUM_DARK = "#162b5d"


def _format(
    width: float = GOLDEN_SLIDE["width"],
    fraction_of_line_width: float = 1,
    ratio: float = (5**0.5 - 1) / 2,
) -> None:
    """Fetches information from current pyplot to verify and impose format.

    Args:
        plt (matplotlib.pyplot): Pyplot object
        width (float): Textwidth of the report to make fontsizes match.
        fraction_of_line_width (float, optional): Fraction of the document width
            which you wish the figure to occupy.  Defaults to 1.
        ratio (float, optional): Fraction of figure width that the figure height
            should be. Defaults to (5 ** 0.5 - 1)/2.

    Returns:
        None: alters plt to ensure good formatting.
    """
    fig = plt.gcf()
    axes = fig.axes

    for ax in axes:
        if ax.get_title() == "":
            warnings.warn("Title is not specified!")
        if ax.get_xlabel() == "":
            warnings.warn("X-axis label not specified!")
        if ax.get_ylabel() == "":
            warnings.warn("Y-axis label not specified!")

        # Format snake_case to Capitalized case
        new_xlabel = " ".join(ax.get_xlabel().split("_")).capitalize()
        ax.set_xlabel(new_xlabel)

        new_ylabel = " ".join(ax.get_ylabel().split("_")).capitalize()
        ax.set_ylabel(new_ylabel)

    set_dim(fig, width=width, fraction_of_line_width=fraction_of_line_width, ratio=ratio)

    plt.tight_layout()


# Extend `matplotlib.pyplot` with `_format` method
plt.format = _format
