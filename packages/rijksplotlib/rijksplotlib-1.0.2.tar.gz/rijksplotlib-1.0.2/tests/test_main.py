"""Tests the main module of the rijksplotlib package."""
import logging
import rijksplotlib as rpl


def test_create_logger(caplog):
    """Test the create_logger function."""
    rpl.create_logger()
    log = logging.getLogger(__name__)
    log.warning("Testing the create_logger function.")
    assert "Testing the create_logger function." in caplog.text
    caplog.clear()

    log.info("Info level should not be logged.")
    assert caplog.text == ""
