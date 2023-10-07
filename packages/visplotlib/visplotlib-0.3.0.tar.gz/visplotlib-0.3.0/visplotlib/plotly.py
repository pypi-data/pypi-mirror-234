"""Visplotlib plotly module."""
import os
import warnings

import plotly
import plotly.express as px  # pylint: disable = unused-import; noqa: F401
import plotly.graph_objects as go

from .dims import GOLDEN_SLIDE

# import plotly express
# pylint: disable=R0912


filepath = os.path.dirname(os.path.abspath(__file__))


def _create_fullsize_template(ratio: float = 9 / 4.3) -> go.layout.Template:
    """Create a fullsize template for plotly figures so that they can be inserted easily in google slides.

    Args:
        ratio(float): ratio between width and height of the figure. Default is 9/4.3. Must be the
        same as the one in the google slide template.

    Returns:
        (go.layout.Templat): template for plotly figures
    """
    fullsize_template = go.layout.Template()

    fullsize_template.layout = {
        "font": {"family": "Lato", "size": 67, "color": "#162b5d"},
        "legend": {"font": {"size": 67, "color": "#162b5d"}},
        "autosize": False,
        "width": 2500 * ratio,
        "height": 2500,
        "margin": {"l": 375, "r": 250, "b": 375, "t": 375, "pad": 75},
        "paper_bgcolor": "White",
    }
    return fullsize_template


def _create_halfize_template(ratio: float = 4.5 / 2.15) -> go.layout.Template:
    """Create a halfsize template for plotly figures so that they can be inserted easily in google slides.

    Args:
        ratio(float): ratio between width and height of the figure. Default is 9/4.3. Must be the
        same as the one in the google slide template.

    Returns:
        (go.layout.Templat): template for plotly figures
    """
    half_size_template = go.layout.Template()

    half_size_template.layout = {
        "font": {"family": "Lato", "size": 107, "color": "#162b5d"},
        "legend": {"font": {"size": 107, "color": "#162b5d"}},
        "autosize": False,
        "width": 2000 * ratio,
        "height": 2000,
        "margin": {"l": 487, "r": 325, "b": 487, "t": 487, "pad": 75},
        "paper_bgcolor": "White",
    }
    return half_size_template


def _create_default_template() -> go.layout.Template:
    """Create a default template for plotly figures that is notebook friendly.

    Returns:
        (go.layout.Templat): template for plotly figures
    """
    default_template = go.layout.Template()

    default_template.layout = {
        "font": {"family": "Lato", "size": 15, "color": "#162b5d"},
        "legend": {"font": {"size": 15, "color": "#162b5d"}},
        "autosize": False,
        "width": GOLDEN_SLIDE["width"] * 1.34,
        "height": GOLDEN_SLIDE["width"],
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
        "paper_bgcolor": "White",
    }

    return default_template


def make_text_bold(fig: go.layout.Template) -> go.layout.Template:
    """Make all the text bold in a plotly figure.

    Args:
        fig ( go.layout.Template):  plotly figure

    Returns:
         go.layout.Template: plotly figure
    """
    if fig.layout.xaxis.title.text is not None:
        fig.layout.xaxis.title.text = "<b>" + fig.layout.xaxis.title.text + "</b>"
    if fig.layout.yaxis.title.text is not None:
        fig.layout.yaxis.title.text = "<b>" + fig.layout.yaxis.title.text + "</b>"
    if fig.layout.title.text is not None:
        fig.layout.title.text = "<b>" + fig.layout.title.text + "</b>"
    return fig


def _format(  # noqa: E501, C901,
    fig: plotly.graph_objs.Figure,
    template_type: str = "default",
) -> None:
    """Fetches information from current pyplot to verify and impose format.

    Args:
        fig (plotly.graph_objs.Figure): plotly object
        template_type (str): Select if a "fullsize", "halfsize", or "notebook" template is desired.
        defaults to "fullsize".

    Returns:
        None: alters plt to ensure good formatting.
    """
    subgraph_num = len([x for x in fig.to_dict()["layout"].keys() if "xaxis" in x])

    if fig.layout.title.text is None:
        warnings.warn("Title is not specified!")
    else:
        new_title = " ".join(fig.layout.title.text.split("_")).capitalize()
        fig.update_layout(title=new_title, title_font_color="#162b5d")

    if fig.layout.legend:
        fig.update_layout(legend_font_color="#162b5d")

    if subgraph_num == 1:
        if fig.layout.xaxis.title.text is None:
            warnings.warn("X-axis label not specified!")
        else:
            new_xlabel = " ".join(fig.layout.xaxis.title.text.split("_")).capitalize()
            fig.update_layout(xaxis_title=new_xlabel)

        if fig.layout.yaxis.title.text is None:
            warnings.warn("Y-axis label not specified!")
        else:
            new_ylabel = " ".join(fig.layout.yaxis.title.text.split("_")).capitalize()
            fig.update_layout(yaxis_title=new_ylabel)

    else:
        if fig.layout.xaxis.title.text is None:
            warnings.warn("X-axis label of subgraph 1 not specified!")
        if fig.layout.yaxis.title.text is None:
            warnings.warn("Y-axis label of subgraph 1 not specified!")

        for i in range(2, subgraph_num + 1):
            if fig.layout[f"xaxis{i}"].title.text is None:
                warnings.warn(f"X-axis label of subgraph {i} label not specified!")
            else:
                new_xlabel = " ".join(fig.layout[f"xaxis{i}"].title.text.split("_")).capitalize()
                fig.layout[f"xaxis{i}"].title.text = new_xlabel

            if fig.layout[f"yaxis{i}"].title.text is None:
                warnings.warn(f"Y-axis label of subgraph {i} not specified!")
            else:
                new_ylabel = " ".join(fig.layout[f"yaxis{i}"].title.text.split("_")).capitalize()
                fig.layout[f"yaxis{i}"].title.text = new_xlabel

    if template_type == "fullsize":
        template = _create_fullsize_template()
    elif template_type == "halfsize":
        template = _create_halfize_template()
    elif template_type == "default":
        template = _create_default_template()
    else:
        error_text = "template_type must be either 'fullsize', 'halfsize', or 'default', not " + f"{template_type}"
        raise ValueError(error_text)
    fig.update_layout(
        template=template,
    )
    fig = make_text_bold(fig)


plotly.format = _format
