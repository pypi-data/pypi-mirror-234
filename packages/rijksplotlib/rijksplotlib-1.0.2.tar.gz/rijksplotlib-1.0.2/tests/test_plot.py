"""Test the plot module of the rijksplotlib package."""
import matplotlib.pyplot as plt
import pytest

import rijksplotlib as rpl
import rijksplotlib.pyplot as rlt

from tests import append_space, test_histogram


@pytest.fixture(autouse=True)
def clear_matplotlib_figure():
    """Automatically clear the matplotlib figure after every test."""
    yield
    plt.clf()


def test_show():
    """Test the rlt.show function."""
    test_histogram()
    rlt.show(block=False)


def test_title():
    """Test the rlt.title function."""
    input_str = "<Blauw:blue> is een mooie kleur maar <roze:#FD96B4> is mooier"
    fig = plt.gcf()
    rlt.title(input_str, default_color="black")

    matplotlib_text = "".join([text.get_text() for text in fig.texts])
    expected_text = append_space("Blauw is een mooie kleur maar roze is mooier")
    assert matplotlib_text == expected_text

    blue_text = fig.texts[0]
    assert blue_text.get_text() == append_space("Blauw")
    assert blue_text.get_color() == "blue"

    # Check default text color
    second_word = fig.texts[1]
    assert second_word.get_text() == append_space("is")
    assert second_word.get_color() == "black"

    pink_text = fig.texts[6]
    assert pink_text.get_text() == append_space("roze")
    assert pink_text.get_color() == "#FD96B4"


def test_empty_title():
    """Test the rlt.title function with an empty string."""
    input_str = ""
    fig = plt.gcf()
    rlt.title(input_str)

    title_texts = [text for text in fig.texts if text.get_gid() == "rws-title"]
    assert len(title_texts) == 0


def test_subtitle():
    """Test the subtitle function."""
    fig = plt.gcf()
    # Create a title first since we can't create a subtitle without a title
    rlt.title("Title")

    subtitle_input = "New subtitle"
    rlt.subtitle(subtitle_input)
    subtitle_texts = [
        text.get_text() for text in fig.texts if text.get_gid() == "rws-subtitle"
    ]
    # rlt.subtitle slices the input into a list of strings (each one ending with a space)
    # E.g. "New title" becomes ["New ", "title "], which will become "New title " when joined
    # we then remove the last space to get the original string
    subtitle_output = "".join(subtitle_texts).rstrip()
    assert subtitle_input == subtitle_output


def test_empty_subtitle():
    """Test the rlt.subtitle function with an empty string."""
    input_str = ""
    fig = plt.gcf()
    rlt.title("Title")
    rlt.subtitle(input_str)
    subtitle_texts = [text for text in fig.texts if text.get_gid() == "rws-subtitle"]
    assert len(subtitle_texts) == 0


def test_subtitle_without_title():
    """Test the rlt.subtitle function without a title."""
    with pytest.raises(ValueError):
        rlt.subtitle("Subtitle")


def test_long_figtext():
    """Test the dv.plot.figtext function with a long string."""
    fig = plt.gcf()
    input_str = (
        "This is a very long string that should be split into multiple lines"
        " because it is too long to fit on one line"
        " and it should be split at spaces"
    )

    text_block_height = rlt.figtext(
        input_str, default_color="black", lineheight_inches=0.1
    )
    assert text_block_height == pytest.approx(0.2, abs=0.01)
    assert len(fig.texts) == len(input_str.split(" "))
