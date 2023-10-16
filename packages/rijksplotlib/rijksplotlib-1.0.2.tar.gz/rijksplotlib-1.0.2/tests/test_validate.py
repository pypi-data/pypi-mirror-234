import matplotlib.pyplot as plt
import pytest
import numpy as np
import logging
import rijksplotlib as rpl
import rijksplotlib.pyplot as rlt

from rijksplotlib.validate import validate_graph, ERROR_MESSAGES

LOGGER = logging.getLogger(__name__)


def setup_graph() -> tuple[plt.Figure, plt.Axes]:
    """Create a simple lineplot."""
    x = np.arange(0, 10, 0.1)
    y = np.sin(x)

    fig, ax = plt.subplots()
    plt.plot(x, y)

    return fig, ax


@pytest.fixture(autouse=True)
def clear_matplotlib_figure():
    """Automatically clear the matplotlib figure after every test."""
    yield
    plt.clf()


def test_validate_fig(caplog):
    """Test that validate_graph does not raise an error.

    Parameters
    ----------
    caplog
        The pytest fixture that captures log messages.
    """
    caplog.set_level(logging.INFO)
    _, ax = setup_graph()
    ax.plot([1, 2, 3], label="Inline label")
    rlt.title("This is a title.")
    rlt.source("Bron: Rijkswaterstaat")
    rlt.logo_rwsdatalab()
    rlt.xlabel("This is an xlabel.")
    rlt.ylabel("This is an ylabel.")
    rlt.legend()
    validate_graph()
    assert caplog.text == ""


def test_validate_figsize_logs_when_not_right_figsize(caplog):
    """Test if validate_graph logs when the figure size is not correct.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    fig, _ = setup_graph()
    fig.set_size_inches([1, 1])
    error_message = ERROR_MESSAGES["figsize"]["text"]
    validate_graph(disabled_errors=["figsize"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_figsize_logs_nothing_when_figsize_is_not_changed(caplog):
    """Test if validate_graph logs nothing when the figure size is not changed.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    validate_graph()
    assert ERROR_MESSAGES["figsize"]["text"] not in caplog.text


def test_validate_xlabel_logs_when_not_our_xlabel(caplog):
    """Test if validate_graph logs when the xlabel is not our xlabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    _, ax = setup_graph()
    ax.set_xlabel("This is an xlabel.")
    error_message = ERROR_MESSAGES["xlabel"]["text"]
    validate_graph(disabled_errors=["xlabel"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_xlabel_logs_when_no_xlabel(caplog):
    """Test if validate_graph logs when there is no xlabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    error_message = ERROR_MESSAGES["xlabel"]["text"]
    validate_graph(disabled_errors=["xlabel"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_xlabel_logs_nothing_when_our_xlabel(caplog):
    """Test if validate_graph logs nothing when the xlabel is our xlabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    _, ax = setup_graph()
    rlt.xlabel("This is an xlabel.", ax)
    validate_graph()
    assert ERROR_MESSAGES["xlabel"]["text"] not in caplog.text


def test_validate_ylabel_logs_when_not_our_ylabel(caplog):
    """Test if validate_graph logs when the ylabel is not our ylabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    _, ax = setup_graph()
    ax.set_ylabel("This is an ylabel.")
    error_message = ERROR_MESSAGES["ylabel"]["text"]
    validate_graph(disabled_errors=["ylabel"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_ylabel_logs_when_no_ylabel(caplog):
    """Test if validate_graph logs when there is no ylabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    error_message = ERROR_MESSAGES["ylabel"]["text"]
    validate_graph(disabled_errors=["ylabel"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_ylabel_logs_nothing_when_our_ylabel(caplog):
    """Test if validate_graph logs nothing when the ylabel is our ylabel.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    _, ax = setup_graph()
    rlt.ylabel("This is an ylabel.", ax)
    validate_graph()
    assert ERROR_MESSAGES["ylabel"]["text"] not in caplog.text


def test_validate_xticklabels_rotation_logs_when_labels_are_rotated(caplog):
    """Test if validate_graph logs when the xticklabels are rotated.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    plt.xticks(rotation=45)  # Rotates X-Axis Ticks by 45-degrees
    error_message = ERROR_MESSAGES["xtickrotation"]["text"]
    validate_graph(disabled_errors=["xtickrotation"])
    assert error_message not in caplog.text
    validate_graph()
    assert error_message in caplog.text


def test_validate_xticklabels_rotation_logs_nothing_when_labels_are_horizontal(caplog):
    """Test if validate_graph logs nothing when the xticklabels are horizontal.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    plt.xticks(rotation=0)
    validate_graph()
    assert ERROR_MESSAGES["xtickrotation"]["text"] not in caplog.text


def test_validate_xticklabels_rotation_logs_nothing_when_there_are_no_xticklabels(
    caplog,
):
    """Test if validate_graph logs nothing when there are no xticklabels.

    Parameters
    ----------
    caplog
        The caplog fixture.
    """
    caplog.set_level(logging.INFO)
    setup_graph()
    plt.tick_params(
        left=False, right=False, labelleft=False, labelbottom=False, bottom=False
    )
    validate_graph()
    assert ERROR_MESSAGES["xtickrotation"]["text"] not in caplog.text
