"""Functions to set figure dimensions."""
from typing import Tuple

import matplotlib.pyplot as plt

# Parameters to match Google Slides template
GOLDEN_SLIDE = {"width": 625, "ratio": 0.48}
FULL_SLIDE = {"width": 625, "ratio": 0.48}
TWO_THIRDS_SLIDE = {"width": 430}
BOTTOM_SLIDE = {"width": 625, "ratio": (5**0.5 - 1) / 4}


def get_dim(
    width: float,
    fraction_of_line_width: float = 1,
    ratio: float = (5**0.5 - 1) / 2,
) -> Tuple[float, float]:
    """Return figure height, width in inches to avoid scaling in latex.

    Default aspect ratio is the golden ratio, and a figure size occupying
    full page width. To get the correct text width for your latex document,
    check:
    https://tex.stackexchange.com/questions/39383/determine-text-width

    # TODO:  Add Visium LaTeX report default width and default width for

    Args:
      width (float): Textwidth of the report (in pt) to make fontsizes match.
      fraction_of_line_width (float, optional): Fraction of the document width
        which you wish the figure to occupy. Use e.g. 0.5 for a figure which should
        only fill one column in a double column layout. Defaults to 1.
      ratio (float, optional): Fraction of figure width to figure height.
        Defaults to (5 ** 0.5 - 1)/2.

    Returns:
      fig_dim (tuple):
          Dimensions of figure in inches meant to be passed on directly to
          matplotlib via the `figsize` argument.
    """
    # Width of figure
    fig_width_pt = width * fraction_of_line_width

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


def set_dim(
    fig: plt.figure,
    width: float = GOLDEN_SLIDE["width"],
    fraction_of_line_width: float = 1,
    ratio: float = (5**0.5 - 1) / 2,
) -> None:
    """Set aesthetic figure dimensions to avoid scaling in latex.

    Args:
      fig (plt.figure): Figure object to resize.
      width (float): Textwidth of the report to make fontsizes match.
      fraction_of_line_width (float, optional): Fraction of the document width
        which you wish the figure to occupy.  Defaults to 1.
      ratio (float, optional): Fraction of figure width that the figure height
        should be. Defaults to (5 ** 0.5 - 1)/2.
    """
    fig.set_size_inches(get_dim(width=width, fraction_of_line_width=fraction_of_line_width, ratio=ratio))
