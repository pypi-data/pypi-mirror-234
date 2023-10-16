"""Functionality regarding the validation of the current graph.

This module contains functionality to validate the current graph.
The following checks are performed:

* The graph has a title.
* The graph has an xlabel.
* The graph has a ylabel.
* The graph has a legend.
* The graph has a source.
* The graph has a logo.

.. list-table:: Validation error types
    :widths: 10 70 20
    :header-rows: 1

    * - Error type
      - Message
      - Log level
    * - title
      - Missing a title, use rlt.title('your title')
      - error
    * - xlabel
      - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
      - info
    * - ylabel
      - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
      - info
    * - xtickrotation
      - Don't rotate xticks, try shortening or wrapping the xticklabels if the labels are too long.
      - warning
    * - legend
      - Missing legend, is this correct? If not, use rlt.legend()
      - info
    * - source
      - Missing a source, use rlt.source('your source')
      - warning
    * - logo
      - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')
      - warning
    * - figsize
      - Incorrect figure width, the default figure width (5.35in) is optimized to exactly fit an RWS-report. Re-sizing after generating the figure will result in non-matching font sizes.
      - warning
"""  # noqa: B950
import logging
from typing import Optional

from matplotlib import pyplot as plt
from numpy.testing import assert_almost_equal

logger = logging.getLogger(__name__)


LOGLEVELS = {
    "critical": 50,
    "error": 40,
    "warning": 30,
    "info": 20,
    "debug": 10,
    "notset": 0,
}
ERROR_MESSAGES = {
    "title": {
        "text": "Missing a title, use rlt.title('your title')",
        "loglevel": LOGLEVELS["error"],
        "order": 0,
    },
    "xlabel": {
        "text": "Missing xlabel, is this correct? If not,"
        " use rlt.xlabel('your xlabel').",
        "loglevel": LOGLEVELS["info"],
        "order": 1,
    },
    "ylabel": {
        "text": "Missing ylabel, is this correct? If not,"
        " use rlt.ylabel('your ylabel').",
        "loglevel": LOGLEVELS["info"],
        "order": 2,
    },
    "xtickrotation": {
        "text": "Don't rotate xticks, try shortening or wrapping the xticklabels"
        " if the labels are too long.",
        "loglevel": LOGLEVELS["warning"],
        "order": 3,
    },
    "legend": {
        "text": "Missing legend, is this correct? If not, use rlt.legend()",
        "loglevel": LOGLEVELS["info"],
        "order": 4,
    },
    "source": {
        "text": "Missing a source, use rlt.source('your source')",
        "loglevel": LOGLEVELS["warning"],
        "order": 5,
    },
    "logo": {
        "text": "Missing a department logo, use rlt.logo_rwsdatalab()"
        " or rlt.logo('My department name')",
        "loglevel": LOGLEVELS["warning"],
        "order": 6,
    },
    "figsize": {
        "text": "Incorrect figure width, the default figure width (5.35in)"
        " is optimized to exactly fit an RWS-report. Re-sizing after generating"
        " the figure will result in non-matching font sizes.",
        "loglevel": LOGLEVELS["warning"],
        "order": 7,
    },
}


def validate_graph(disabled_errors: Optional[list[str]] = None) -> None:
    """Validate the current graph.

    This function checks if the current graph passes the following checks:

    * The graph has a title.
    * The graph has an xlabel.
    * The graph has a ylabel.
    * The graph has a legend.
    * The graph has a source.
    * The graph has a logo.

    Parameters
    ----------
    disabled_errors
        A list of errors to disable. The following errors are available:

        * title
        * source
        * logo
        * figsize
        * xlabel
        * ylabel
        * xtickrotation
    """
    if not disabled_errors:
        disabled_errors = []

    fig = plt.gcf()
    axes = fig.get_axes()

    fig_errors = validate_fig(fig, disabled_errors)
    axes_errors = validate_axes(axes, disabled_errors)
    graph_errors = [*fig_errors, *axes_errors]
    if not graph_errors:
        return

    # Sort the errors by order, since some of the functions recommended
    # have a specific order of execution.
    for error in sorted(graph_errors, key=lambda e: e["order"]):
        logger.log(error["loglevel"], error["text"])


def validate_fig(  # noqa: C901
    fig: plt.Figure, disabled_errors: list[str]
) -> list[dict]:
    """Validate a matplotlib figure.

    Parameters
    ----------
    fig
        A matplotlib figure to validate.
    disabled_errors
        A list of errors to disable. The following errors are available:

        * title
        * source
        * logo
        * figsize

    Returns
    -------
        A list with the errors to log.
    """
    fig_errors = []
    if not _has_title(fig) and "title" not in disabled_errors:
        fig_errors.append(ERROR_MESSAGES["title"])
    if not _has_source(fig) and "source" not in disabled_errors:
        fig_errors.append(ERROR_MESSAGES["source"])
    if not _has_logo(fig) and "logo" not in disabled_errors:
        fig_errors.append(ERROR_MESSAGES["logo"])
    if not _has_designed_figsize_width(fig) and "figsize" not in disabled_errors:
        fig_errors.append(ERROR_MESSAGES["figsize"])

    return fig_errors


def validate_axes(  # noqa: C901
    axes: list[plt.Axes], disabled_errors: list[str]
) -> list[dict]:
    """Validate a list of matplotlib axes.

    Parameters
    ----------
    axes
        A list of matplotlib axes to validate.
    disabled_errors
        A list of errors to disable. The following errors are available:

        * xlabel
        * ylabel
        * xtickrotation
        * legend

    Returns
    -------
        A list with the errors to log.
    """
    # We might have multiple plt.Axes with the same error.
    # We use a dict to prevent duplicate log messages
    # The validate_fig method doesn't have this problem, because there is only one fig.
    ax_errors = {}

    for ax in axes:
        if not _has_xlabel(ax) and "xlabel" not in disabled_errors:
            ax_errors["xlabel"] = ERROR_MESSAGES["xlabel"]
        if not _has_ylabel(ax) and "ylabel" not in disabled_errors:
            ax_errors["ylabel"] = ERROR_MESSAGES["ylabel"]
        if not ax.get_legend() and "legend" not in disabled_errors:
            ax_errors["legend"] = ERROR_MESSAGES["legend"]
        if (
            not _has_horizontal_xticklabels(ax)
            and "xtickrotation" not in disabled_errors
        ):
            ax_errors["xtickrotation"] = ERROR_MESSAGES["xtickrotation"]

    # Convert the dict back to a list
    return list(ax_errors.values())


def _has_title(fig: plt.Figure) -> bool:
    """Check if the graph has a title.

    Parameters
    ----------
    fig
        A matplotlib figure.

    Returns
    -------
        True if a if the figure has a rws title, false otherwise.
    """
    return _fig_has_text_with_gid(fig, "rws-title")


def _has_logo(fig: plt.Figure) -> bool:
    """Check if the graph has a logo.

    Parameters
    ----------
    fig
        A matplotlib figure.

    Returns
    -------
        True if a if the figure has a logo, false otherwise.
    """
    return _fig_has_text_with_gid(fig, "rws-logo")


def _has_source(fig: plt.Figure) -> bool:
    """Check if the graph has a source.

    Parameters
    ----------
    fig
        A matplotlib figure.

    Returns
    -------
        True if a if the figure has a source, false otherwise.
    """
    return _fig_has_text_with_gid(fig, "rws-source")


def _fig_has_text_with_gid(fig: plt.Figure, gid: str) -> bool:
    """Check if the graph has a text with the requested GID.

    Parameters
    ----------
    fig
        A matplotlib figure.

    Returns
    -------
        True if a text with the requested GID is in the figure, false otherwise.
    """
    for text in fig.texts:
        if text.get_gid() == gid:
            return True
    return False


def _has_designed_figsize_width(fig: plt.Figure) -> bool:
    """Check if the graph has the designed figsize.

    Parameters
    ----------
    fig
        A matplotlib figure.

    Returns
    -------
        True if a if the figure has the figsize from the stylesheet, false otherwise.
    """
    designed_figsize = plt.rcParams["figure.figsize"]
    actual_figsize = fig.get_size_inches()
    try:
        assert_almost_equal(designed_figsize[0], actual_figsize[0], decimal=1)
        assert_almost_equal(designed_figsize[1], actual_figsize[1], decimal=1)
    except AssertionError:
        return False
    return True


def _has_xlabel(ax: plt.Axes) -> bool:
    """Check if the graph has a xlabel.

    Parameters
    ----------
    ax
        A matplotlib Axes.

    Returns
    -------
        True if a if the ax has a rws xlabel, false otherwise.
    """
    return ax.xaxis.get_label().get_gid() == "rws-xlabel"


def _has_ylabel(ax: plt.Axes) -> bool:
    """Check if the graph has a ylabel.

    Parameters
    ----------
    ax
        A matplotlib Axes.

    Returns
    -------
        True if a if the ax has a rws ylabel, false otherwise.
    """
    return ax.yaxis.get_label().get_gid() == "rws-ylabel"


def _has_horizontal_xticklabels(ax: plt.Axes) -> bool:
    """Check if the xticklabels are not rotated.

    Parameters
    ----------
    ax
        A matplotlib Axes.

    Returns
    -------
        True if the axis has horizontal xticklabels, False otherwise.
    """
    for xticklabel in ax.get_xticklabels():
        if xticklabel.get_rotation():
            return False
    return True
