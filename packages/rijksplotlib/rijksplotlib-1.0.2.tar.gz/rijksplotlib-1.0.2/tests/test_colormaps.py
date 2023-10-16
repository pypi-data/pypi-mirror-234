"""Test the colormaps module of the rijksplotlib package."""
import matplotlib as mpl
import rijksplotlib as rpl


def test_continuous_cmap_does_not_register():
    cmaps_before = list(mpl.colormaps.keys())
    rpl.colormaps.continuous_cmap(["hemelblauw", "oranje-tint-5"], "test-cmap")
    cmaps_after = list(mpl.colormaps.keys())
    assert cmaps_before == cmaps_after


def test_continuous_cmap_initializes_correctly():
    color1 = "hemelblauw"
    color2 = "oranje-tint-5"
    cmap_name = f"test-continuous-{color1}-{color2}"
    cmap = rpl.colormaps.continuous_cmap([color1, color2], cmap_name)

    assert (
        mpl.colors.to_hex(cmap(float(0))).lower()
        == rpl.color.rijkskleuren[color1].lower()
    )
    assert (
        mpl.colors.to_hex(cmap(float(1))).lower()
        == rpl.color.rijkskleuren[color2].lower()
    )


def test_diverging_cmap_correct_name():
    """Tests if the name of the diverging cmap is correct."""
    cmap = rpl.colormaps.diverging_cmap("hemelblauw", "oranje", "grijs-2", "test-cmap")
    assert cmap.name == "rws:test-cmap"
