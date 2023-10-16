"""A dictionary of colormaps or color cycles that can be used in the rijksplotlib library.

This module contains methods to create various types of colormaps that can be used
in the rijksplotlib library.

We also have :ref:`a user guide for color usage<colors:Colors>` with accompanying API
documentation at :mod:`rijksplotlib.colors`.
"""

from typing import Optional

import matplotlib as mpl
import numpy as np

from rijksplotlib.color import rijkskleuren


def cmap_from_string(
    colorstring: str, name: Optional[str] = None
) -> mpl.colors.ListedColormap:
    """Make a listed colormap from a string of colors spaced by spaces.

    .. note:: The colors are case insensitive and divided by spaces.

    .. note:: The name of the colormap is prefixed with ``rws:``.
            Example:

            >>> cmap = cmap_from_string("hemelblauw grijs-2", name="blauw-grijs")
            >>> cmap.name
            'rws:blauw-grijs'

    Parameters
    ----------
    colorstring
        String of Rijkshuisstijl color names, divided by spaces. Ignores capitalization.
            Example: "mosgroen HEMELBLAUW Blauw Paars-tint-3".
    name
        Name of colormap, by default None

    Returns
    -------
        Listed colormap
    """
    cmap_colors = [rijkskleuren[color.lower()] for color in colorstring.split(" ")]

    cmap_name = f"rws:{name}" if name else None
    cmap = mpl.colors.ListedColormap(colors=cmap_colors, name=cmap_name)
    return cmap


def diverging_cmap(
    color1: str,
    color2: str,
    mid: str = "donkergeel-tint-4",
    name: Optional[str] = None,
) -> mpl.colors.ListedColormap:
    """Make diverging colormap using Rijkshuisstijl colors.

    Parameters
    ----------
    color1
        One of the rijkshuisstijl colors.
    color2
        One of the rijkshuisstijl colors.
    mid
        Middle color, by default "donkergeel-tint-4"
    name
        Name, by default None, which will result in "rws:{Color1}{Color2}"

    Returns
    -------
        Listed color map
    """
    color1 = color1.lower()
    color2 = color2.lower()

    colorrange1 = [color1.lower()] + [f"{color1}-tint-{num}" for num in np.arange(1, 6)]
    colorrange2 = [f"{color2}-tint-{num}" for num in np.arange(1, 6)[::-1]] + [color2]

    colorstrings = colorrange1 + [mid] + colorrange2
    cmap_colors = [rijkskleuren[c] for c in colorstrings]

    if name:
        cmap_name = name
    else:
        cmap_name = color1.capitalize() + color2.capitalize()

    cmap = mpl.colors.ListedColormap(colors=cmap_colors, name=f"rws:{cmap_name}")
    return cmap


def continuous_cmap(
    colornames: list[str], name: Optional[str] = None
) -> mpl.colors.LinearSegmentedColormap:
    """Make continuous cmap from Rijkshuisstijl colors and its reversed variant.

    Creates a continuous colormap from a list of Rijkshuisstijl colors.
    The colors are interpolated linearly.

    Parameters
    ----------
    colornames
        List of at least two Rijkshuisstijl colors, for example ['hemelblauw', 'grijs-2'].
    name
        Name to register the colormap, by default None (unregistered).
        Will be formatted as "rws:{name}"

    Returns
    -------
        LinearSegmentedColormap
    """
    cmap_name = f"rws:{name}"
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        cmap_name, colors=[rijkskleuren[colorname] for colorname in colornames]
    )

    return cmap


def _cmap_PBL_categorisch() -> mpl.colors.ListedColormap:
    """Make PBL categorische colormap.

    Create a categorical colormap with the colors used by PBL.
    You can use this colormap by calling ``plt.get_cmap("rws:PBL_categorisch")``.

    .. warning:: This function is not intended to be used by the user.
        Since it is used in the ``__init__.py`` file of the
        rijksplotlib library, the colormap is automatically
        registered when the library is imported.

    Returns
    -------
        Listed colormap
    """
    colorstring = (
        "Hemelblauw Mosgroen Violet Donkergeel Paars "
        "Lichtblauw Roze Groen Rood Donkergroen Oranje Donkerbruin "
        "Robijnrood Bruin Mintgroen Geel"
    )
    cmap = cmap_from_string(colorstring, name="PBL_categorisch")
    return cmap


def _cmap_RWS_categorisch() -> mpl.colors.ListedColormap:
    """Make RWS categorische colormap.

    Create a categorical colormap with the colors used by Rijkswaterstaat.
    You can use this colormap by calling ``plt.get_cmap("rws:categorisch")``.

    .. warning:: This function is not intended to be used by the user.
        Since it is used in the ``__init__.py`` file of the
        rijksplotlib library, the colormap is automatically
        registered when the library is imported.

    Returns
    -------
        Listed colormap
    """
    colorstring = "hemelblauw donkergeel paars oranje roze mosgroen robijnrood"
    cmap = cmap_from_string(colorstring, name="categorisch")
    return cmap


def __overlay_cmaps() -> list[mpl.colors.ListedColormap]:
    """Make overlay colormaps.

    .. warning:: This function is not intended to be used by the user.
        Since it is used in the ``__init__.py`` file of the
        rijksplotlib library, the colormaps are automatically
        registered when the library is imported.

    Returns
    -------
        A list of ListedColormaps used by the overlay plots.
    """
    cmaps = [
        cmap_from_string("wit mintgroen groen grijs-5", name="overlay-groen"),
        cmap_from_string("wit lichtblauw hemelblauw grijs-5", name="overlay-blauw"),
        cmap_from_string("wit violet-tint-1 paars grijs-5", name="overlay-paars"),
        cmap_from_string("wit geel-tint-1 donkergeel grijs-5", name="overlay-geel"),
    ]
    return cmaps


def __continuous_cmaps() -> list[mpl.colors.LinearSegmentedColormap]:
    """Create a list of continuous colormaps.

    .. warning:: This function is not intended to be used by the user.
            Since it is used in the ``__init__.py`` file of the
            rijksplotlib library, the colormaps are automatically
            registered when the library is imported.

    Returns
    -------
        A list of LinearSegmentedColormaps.
    """
    cmaps = [
        continuous_cmap(
            ["donkerblauw", "hemelblauw", "lichtblauw", "grijs-2"],
            name="continuous-blauw",
        ),
        continuous_cmap(["paars", "grijs-2"], name="continuous-paars"),
        continuous_cmap(["groen", "grijs-2"], name="continuous-groen"),
        continuous_cmap(
            ["violet", "robijnrood-tint-3", "grijs-2"], name="continuous-violet"
        ),
    ]
    return cmaps


def __diverging_cmaps() -> list[mpl.colors.ListedColormap]:
    """Create a list of diverging colormaps.

    .. warning:: This function is not intended to be used by the user.
        Since it is used in the ``__init__.py`` file of the
        rijksplotlib library, the colormaps are automatically
        registered when the library is imported.

    Returns
    -------
        A list of ListedColormaps.
    """
    cmaps = [
        diverging_cmap("violet", "mosgroen"),
        diverging_cmap(
            "robijnrood",
            "hemelblauw",
            mid="grijs-2",
        ),
    ]
    return cmaps


def _register_cmaps() -> None:
    """Register default colormaps on init of package.

    .. warning:: This function is not intended to be used by the user.
        Since it is used in the ``__init__.py`` file of the
        rijksplotlib library, the colormaps are automatically
        registered when the library is imported.
    """
    mpl.colormaps.register(_cmap_RWS_categorisch(), force=True)
    mpl.colormaps.register(_cmap_PBL_categorisch(), force=True)
    for cmap in __diverging_cmaps():
        mpl.colormaps.register(cmap, force=True)
        mpl.colormaps.register(cmap.reversed(), force=True)
    for cmap in __overlay_cmaps():
        mpl.colormaps.register(cmap, force=True)
    for cmap in __continuous_cmaps():
        mpl.colormaps.register(cmap, force=True)
        mpl.colormaps.register(cmap.reversed(), force=True)
