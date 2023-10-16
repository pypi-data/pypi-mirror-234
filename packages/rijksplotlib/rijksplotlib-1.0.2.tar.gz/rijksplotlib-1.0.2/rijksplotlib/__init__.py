# -*- coding: utf-8 -*-
"""Documentation about rijksplotlib

This module contains the ``rijksplotlib`` package. This package contains a set of
functions and classes that can be used to create plots in a consistent way.
This package tightly integrates with matplotlib and seaborn, and provides
linting-like functionality to ensure that plots are created in a consistent
manner.

The import style of this package is also similar to that of matplotlib and
seaborn. The recommended import style is:

.. code-block:: python

    import rijksplotlib as rpl
    import matplotlib as mpl

    import matplotlib.pyplot as plt
    import rijksplotlib.pyplot as rlt

.. warning::

    Although this module mirrors the import structure of ``matplotlib`` we do not fully wrap it.
    If you want to use a function that is not available in ``rijksplotlib``, you can always use the
    ``matplotlib`` module directly.

----
"""

import logging
import os
import sys

from logginginitializer.logging_config import LoggingConfig
from logginginitializer.logging_initializer import LoggingInitializer

# Reexport modules
import rijksplotlib.colormaps as colormaps
import rijksplotlib.pylint_rules as pylint_rules
import rijksplotlib.pyplot as pyplot
import rijksplotlib.stylesheets as stylesheets
import rijksplotlib.utils as utils

# Set the info of the package
__author__ = "RWS Datalab"
__email__ = "datalab.codebase@rws.nl"
__version__ = "1.0.2"


def create_logger() -> None:
    """Create a logger for the package.

    This function creates a logger for the package. The logger is configured
    using the ``LoggingConfig`` class from the ``logginginitializer`` package.
    This logger is used to log messages from the package. The logger is
    configured to log to the console, and to log messages with the level
    ``INFO`` or higher.
    """
    logging_config = LoggingConfig(identifier="rijksplotlib", directory="")

    # TODO: Update to latest version of logginginitializer so that we can disable log files and only use stdout.
    # Don't use LoggingInitializer since we can't disable log file saving.
    # And we only need the console output.
    logging.basicConfig(
        level=logging_config.log_level,
        format=logging_config.log_format,
        datefmt=logging_config.date_format,
        handlers=[logging.StreamHandler()],
    )


def is_notebook() -> bool:
    """Check if we are running in a notebook.

    This function checks if we are running in a notebook by checking if the
    ``get_ipython`` function is available. If it is available, we check if the
    shell is a ``ZMQInteractiveShell``. If so, we are running in a notebook.

    Returns
    -------
        bool
            True if we are running in a notebook, False otherwise.
    """
    try:
        # get_ipython is imported already by IPython, so we don't need to import it
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined]
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


create_logger()
# Register functions on import
stylesheets.apply_stylesheet()
colormaps._register_cmaps()

# If we are in a notebook, log a warning message
if is_notebook():
    logger = logging.getLogger(__name__)
    logger.warning(
        "You are running in a Jupyter Notebook, please ensure to always use rlt.show()"
        " at the end of your plotting cells."
    )
