"""Util functions for the rijksplotlib package."""
import os
import re
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt


def resolve_path(path: str = "") -> Path:
    """Resolve a path relative to the root project directory.

    .. warning:: This function only works if you cloned the repository
        without changing the name of the repository. The examples,
        docs etc should be run from inside the outer rijksplotlib
        directory. If it's not, this function will not work.

    Parameters
    ----------
    path
        The subpath to resolve, leave empty to get the root project directory.

    Returns
    -------
        An absolute path to the subpath.
    """
    root, package_name, _ = os.getcwd().partition("rijksplotlib")
    fullpath = Path(root) / package_name / path
    return fullpath


def split_between_brackets(text: str) -> list[str]:
    """Split a string on < and >, but keep the < and > in the result.

    Example
    -------
    >>> split_between_brackets("This is <some> text")
    ["This is ", "<some>", " text"]

    Parameters
    ----------
    text
        The string to be split.

    Returns
    -------
    A list of strings that were split on < and >.
    """
    matches = re.findall(r"<[^>]+>|[^<>]+", text)
    return [match.strip() for match in matches if match.strip()]


def get_fontsize_points(font_scaling="medium") -> float:
    """Get the fontsize in points of a certain font scaling.

    Parameters
    ----------
    font_scaling
        One of the matplotlib font scalings:

        * xx-small
        * x-small
        * small
        * medium
        * large
        * x-large
        * xx-large
        * larger
        * smaller

        by default "medium"
    """
    font_scalings = {
        "xx-small": 0.579,
        "x-small": 0.694,
        "small": 0.833,
        "medium": 1.0,
        "large": 1.200,
        "x-large": 1.440,
        "xx-large": 1.728,
        "larger": 1.2,
        "smaller": 0.833,
        None: 1.0,
    }

    fontsize_points = plt.rcParams["font.size"] * font_scalings[font_scaling]
    return fontsize_points


def get_lineheight_points(font_scaling="medium") -> float:
    """Get the line height in points of a certain font scaling (1.03 x fontsize).

    Example
    -------
    >>> get_lineheight_points("medium")
    9.0

    Parameters
    ----------
    font_scaling
        One of the matplotlib font scalings:

        * xx-small
        * x-small
        * small
        * medium
        * large
        * x-large
        * xx-large
        * larger
        * smaller

        by default "medium".

    Returns
    -------
    fontsize in points
    """
    fontsize_points = get_fontsize_points(font_scaling)
    return fontsize_points * 1.3


def points_to_inches(points: float) -> float:
    """Convert measurement in points to inches.

    Parameters
    ----------
    points
        measurement in points

    Returns
    -------
        measurement in inches
    """
    return points / 72


def inches_to_points(inches: float) -> float:
    """Convert measurement in inches to points.

    Parameters
    ----------
    inches
        measurement in inches

    Returns
    -------
        measurement in points
    """
    return inches * 72


def get_top_margin(current_figure: Optional[plt.Figure] = None) -> float:
    """Get the top margin of the current figure.

    Parameters
    ----------
    current_figure
        The figure to get the margin for, default plt.gcf().

    Returns
    -------
    The top margin as a float.
    """
    if not current_figure:
        current_figure = plt.gcf()
    return current_figure.subplotpars.top


def get_bottom_margin(current_figure: Optional[plt.Figure] = None) -> float:
    """Get the bottom margin of the current figure.

    Parameters
    ----------
    current_figure
        The figure to get the margin for, default plt.gcf().

    Returns
    -------
    The bottom margin as a float.
    """
    if not current_figure:
        current_figure = plt.gcf()
    return current_figure.subplotpars.bottom


def get_right_margin(current_figure: Optional[plt.Figure] = None) -> float:
    """Get the right margin of the current figure.

    Parameters
    ----------
    current_figure
        The figure to get the margin for, default plt.gcf().

    Returns
    -------
    The right margin as a float.
    """
    if not current_figure:
        current_figure = plt.gcf()
    return current_figure.subplotpars.right


def increase_top_margin(
    inches_to_add: float | int, current_figure: Optional[plt.Figure] = None
) -> None:
    """
    Increase the top margin of the current figure.

    Parameters
    ----------
    inches_to_add
        The number of inches that are added.
    current_figure
        The figure to increase the margin for, default plt.gcf().
    """
    if not current_figure:
        current_figure = plt.gcf()
    old_top_margin = get_top_margin()
    size = current_figure.get_size_inches()  # size in pixels
    current_figure.subplots_adjust(top=old_top_margin - (inches_to_add / size[1]))


def increase_bottom_margin(
    inches_to_add: float | int, current_figure: Optional[plt.Figure] = None
) -> None:
    """
    Increase the bottom margin of the current figure.

    Parameters
    ----------
    inches_to_add
        The number of inches that are added.
    current_figure
        The figure to increase the margin for, default plt.gcf().
    """
    if not current_figure:
        current_figure = plt.gcf()
    old_bottom_margin = get_bottom_margin()
    size = (
        current_figure.get_size_inches()
    )  # TODO: use get_figheight? Dan hoef je niet size[1] te doen
    current_figure.subplots_adjust(bottom=old_bottom_margin + (inches_to_add / size[1]))


def increase_right_margin(
    inches_to_add: float | int, current_figure: Optional[plt.Figure] = None
) -> None:
    """
    Increase the right margin of the current figure.

    Parameters
    ----------
    inches_to_add
        The number of inches that are added.
    current_figure
        The figure to increase the margin for, default plt.gcf().
    """
    if not current_figure:
        current_figure = plt.gcf()
    old_right_margin = get_right_margin()
    figwidth = current_figure.get_figwidth()
    current_figure.subplots_adjust(right=old_right_margin - (inches_to_add / figwidth))


def get_text_color(text: str, default_color: str) -> tuple[str, str]:
    """Retrieve the text and color from a substring.

    Example
    -------
    >>> get_text_color("<some text:red>", "black")
    ("some text", "red")

    Parameters
    ----------
    text
        The text to be added, if it contains a
        substring with the format <text:color> the
        text will be colored accordingly.
    default_color
        The default color to apply to the text if no
        formatting syntax is used.

    Returns
    -------
    A tuple containing the text and the color.
    """
    color = default_color

    # If the substring starts with < and ends with >
    # it is a word that needs to be colored
    if text[0] == "<" and text[-1] == ">":
        # Split the substring into the word and the color
        # Remove the < and > from the substring before splitting
        text, color = text[1:-1].split(":")

    return text, color
