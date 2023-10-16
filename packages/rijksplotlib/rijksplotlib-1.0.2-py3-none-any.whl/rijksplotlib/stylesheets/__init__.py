"""This module contains matplotlib stylesheet functionality.

It contains both the stylesheets itself in the form of a .mplstyle file,
as well as a function to apply the stylesheet to a matplotlib graph.
The :func:`rijksplotlib.stylesheets.apply_stylesheet` function is used
in the ``__init__.py`` file of the rijksplotlib library, so that the
stylesheet is automatically applied when the library is imported.
"""
from pathlib import Path

import matplotlib.pyplot as plt


def apply_stylesheet() -> None:
    """Apply the matplotlib stylesheet.

    This function applies the matplotlib stylesheet (``rws_report.mplstyle``)
    that is included in this module.

    .. warning:: This function is not intended to be used by the user.
            Since it is used in the ``__init__.py`` file of the
            rijksplotlib library, the stylesheet is automatically
            applied when the library is imported.
    """
    # Run this during module import
    path = Path(__file__).parent
    plt.style.use(path / "rws_report.mplstyle")
