"""A module containing plotting functionality.

This module contains functions to add titles, subtitles, sources, logos and
legends to a graph. It also contains functions to show and save a graph.
In essence this module closely mirrors the usage of ``matplotlib.pyplot``.

The import style is also very similar to ``matplotlib.pyplot``:

.. code-block:: python

    # Just change `matplotlib` to `rijksplotlib`
    # And change `plt` to `rlt` and you're good to go!
    import matplotlib.pyplot as plt
    import rijksplotlib.pyplot as rlt

.. warning::

    Although this module is called ``pyplot``, it does not fully wrap the
    ``matplotlib.pyplot`` module. It only contains a subset of the functions
    that are available in ``matplotlib.pyplot``. If you want to use a function
    that is not available in ``rijksplotlib.pyplot``, you can always use the
    ``matplotlib.pyplot`` module directly.

----
"""
from typing import Optional

import matplotlib as mpl
import matplotlib.axes
import matplotlib.pyplot as plt
from matplotlib import transforms

from rijksplotlib.color import rijkskleuren
from rijksplotlib.utils import (
    get_bottom_margin,
    get_fontsize_points,
    get_lineheight_points,
    get_right_margin,
    get_text_color,
    get_top_margin,
    inches_to_points,
    increase_bottom_margin,
    increase_right_margin,
    increase_top_margin,
    points_to_inches,
    split_between_brackets,
)
from rijksplotlib.validate import _has_title, validate_graph

PADDING_BETWEEN_GRAPH_AND_TITLE_POINTS = get_fontsize_points() * 2


def show(*args, disabled_errors: Optional[list[str]] = None, **kwargs) -> None:
    """Show the graph and validate it.

    This function will validate the graph before showing it, and will log
    warnings or errors if the graph is invalid. It is important to note that
    this function will not prevent an invalid graph from being shown. It will
    only log errors.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.show()
    ERROR:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

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
    *args
        Arguments that will be passed to ``matplotlib.pyplot.show()``.
    **kwargs
        Keyword arguments that will be passed to ``matplotlib.pyplot.show()``.
    """  # noqa: B950
    if not disabled_errors:
        disabled_errors = []

    validate_graph(disabled_errors)
    plt.show(*args, **kwargs)


def savefig(*args, **kwargs) -> None:
    """Save the graph and validate it.

    This function will validate the graph before saving it to disk.
    It is important to note that this function will not prevent an invalid
    graph from being saved to disk. It will only log errors.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.savefig('my_graph.png')
    ERROR:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 13:50:15 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    *args
        Arguments that will be passed to ``matplotlib.pyplot.savefig()``.
    **kwargs
        Keyword arguments that will be passed to ``matplotlib.pyplot.savefig()``.
    """  # noqa: B950
    validate_graph()
    plt.savefig(*args, **kwargs)


def figtext(  # noqa: C901
    text: str,
    default_color: str,
    x: float = 0,
    y: float = 1,
    lineheight_inches: float = 0.1,
    fig: plt.Figure = None,
    **kwargs,
) -> float:
    """
    Add text to the current figure.

    If the text is too long, the text gets wrapped. Colors can be added by
    using the following syntax: ``"Hi this is <red:red> and this is <blue:blue>"``.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> rlt.figtext('This is a <cool:#b8c6d5> title', default_color='black', x=0.5, y=0.5)
    >>> rlt.show()
    ERROR:2023/09/06 13:54:52 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    WARNING:2023/09/06 13:54:52 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 13:54:52 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    text
        The text to be added. Use formatting like <text:color> for colored words.
    default_color
        The color of the text.
    x
        The x position as a fraction of the figure width (between [0,1]). 0 by default.
    y
        The y position as a fraction of the figure height (between [1,0]). 1 by default.
    lineheight_inches
        The height of a text line.
    fig
        The figure to place the text in, default plt.gcf().
    **kwargs
        Keyword arguments that will be passed to `matplotlib.pyplot.figtext`.

    Returns
    -------
    text_block_height_inches
        height of the (wrapped) text block in inches (float).
    """  # noqa: B950
    text_block_height_inches = lineheight_inches

    if not fig:
        fig = plt.gcf()
    renderer = fig.canvas.get_renderer()
    fig_width, fig_height = fig.get_size_inches()
    fig_width *= 0.95
    coordinate_system = fig.dpi_scale_trans

    text_parts = split_between_brackets(text)
    for text_part in text_parts:
        text_part, color = get_text_color(text_part, default_color)

        words = text_part.split()
        for word in words:
            mpl_text = plt.figtext(
                x=x,
                y=fig_height * y,
                s=f"{word} ",
                color=color,
                ha="left",
                va="top",
                clip_on=False,
                transform=coordinate_system,
                figure=fig,
                **kwargs,
            )

            # Get the width of the text in inches
            extent = mpl_text.get_window_extent(renderer=renderer)
            text_width = extent.width / fig.dpi

            # If the text is too long, wrap it
            if x + text_width > fig_width:
                x = 0
                coordinate_system = transforms.offset_copy(
                    mpl_text._transform, fig=fig, y=-lineheight_inches, units="inches"
                )
                text_block_height_inches += lineheight_inches
            else:
                x += text_width

    return text_block_height_inches


def title(
    text: str,
    x: float = 0,
    y: float = 1,
    default_color: Optional[str] = None,
    fig: plt.Figure = None,
    **kwargs,
) -> None:
    """Add a title with formatting.

    .. warning:: If the title/subtitle doesn't show up when calling
        :func:`rijksplotlib.pyplot.show`, it might be due to your
        main window resolution. :func:`rijksplotlib.pyplot.savefig`
        doesn't have this problem.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> rlt.title('This is a <cool:#b8c6d5> title', x=0.5, y=0.5)
    >>> rlt.show()
    WARNING:2023/09/06 14:01:01 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:01:01 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    text
        The title to be added, you can add word formatting by doing the following:
        "This is a <cool:#b8c6d5> subtitle" will make the word "cool" lightblue.
    x
        The x position as a fraction of the figure width (between [0,1]. 0 by default.
    y
        The x position as a fraction of the figure height (between [1,0]. 1 by default.
    fig
        The figure to place the title in, default plt.gcf().
    **kwargs
        Keyword arguments that will be passed on to `matplotlib.pyplot.figtext`.
    """  # noqa: B950
    if not text:
        return
    if not fig:
        fig = plt.gcf()

    fig.subplots_adjust(top=1)  # Start clean: remove top margin
    increase_top_margin(points_to_inches(PADDING_BETWEEN_GRAPH_AND_TITLE_POINTS), fig)

    fontsize = "medium"
    lineheight_inches = points_to_inches(get_lineheight_points(fontsize))

    color = plt.rcParams["axes.titlecolor"]
    if default_color:
        color = default_color

    text_block_height_inches = figtext(
        text,
        color,
        x,
        y,
        lineheight_inches=lineheight_inches,
        fontsize=fontsize,
        fontweight="bold",
        gid="rws-title",
        fig=fig,
        **kwargs,
    )

    increase_top_margin(text_block_height_inches, fig)


def subtitle(text: str, fig: plt.Figure = None, **kwargs) -> None:
    """Add a subtitle with formatting. First the title should be added.

    .. warning:: You should add a title before adding a subtitle.

    .. warning:: If the title/subtitle doesn't show up when calling
        :func:`rijksplotlib.pyplot.show`, it might be due to your
        main window resolution. :func:`rijksplotlib.pyplot.savefig`
        doesn't have this problem.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.title('This is a <cool:#b8c6d5> title')
    >>> rlt.subtitle('This is a <cool:#b8c6d5> subtitle')
    >>> rlt.show()
    INFO:2023/09/06 14:17:50 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:17:50 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:17:50 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:17:50 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:17:50 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    text
        The subtitle to be added, you can add word formatting by doing the following:
        "This is a <cool:#b8c6d5> subtitle" will make the word "cool" lightblue.
    fig
        The figure to put the subtitle in, default plt.gcf().
    **kwargs'
        Keyword arguments that will be passed on to ``matplotlib.pyplot.figtext``.

    Raises
    ------
    ValueError
        If no title is present.
    """  # noqa: B950
    if not text:
        return

    if not fig:
        fig = plt.gcf()
    if not _has_title(fig):
        raise ValueError("You should add a title before adding a subtitle.")

    fontsize = "small"

    # remove the padding between title and figure to later reapply
    increase_top_margin(-points_to_inches(PADDING_BETWEEN_GRAPH_AND_TITLE_POINTS), fig)

    padding_inches = points_to_inches(get_fontsize_points(fontsize) * 0.3)
    increase_top_margin(padding_inches, fig)

    lineheight_inches = points_to_inches(get_lineheight_points(fontsize))

    color = rijkskleuren["grijs-7"]

    text_block_height_inches = figtext(
        text,
        color,
        y=get_top_margin(fig),
        lineheight_inches=lineheight_inches,
        fontsize=fontsize,
        gid="rws-subtitle",
        fig=fig,
        **kwargs,
    )

    increase_top_margin(text_block_height_inches, fig)
    increase_top_margin(points_to_inches(PADDING_BETWEEN_GRAPH_AND_TITLE_POINTS), fig)


def xlabel(xlabel_text: str, ax: matplotlib.axes.Axes = None, **kwargs) -> None:
    """Set the xlabel.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.xlabel('My xlabel')
    >>> rlt.show()
    ERROR:2023/09/06 14:23:08 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:23:08 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:23:08 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:23:08 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:23:08 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    xlabel_text
        A string containing the text to display as x-axis label.
    ax
        Optianal, the matplotlib Axes to set the xlabel for. If not given,
        the current active Axes will be picked.
    **kwargs
        Keyword arguments that will be passed to `ax.set_xlabel()`.
    """  # noqa: B950
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel(xlabel_text, ha="right", x=1, rotation=0, gid="rws-xlabel", **kwargs)


def ylabel(ylabel_text: str, ax: matplotlib.axes.Axes = None, **kwargs) -> None:
    """Set the ylabel.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.ylabel('My ylabel')
    >>> rlt.show()
    ERROR:2023/09/06 14:24:02 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:24:02 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:24:02 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:24:02 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:24:02 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    ylabel_text
        A string containing the text to display as y-axis label.
    ax
        Optianal, the matplotlib Axes to set the ylabel for. If not given,
        the current active Axes will be picked.
    **kwargs
        Keyword arguments that will be passed to `ax.set_ylabel()`.
    """  # noqa: B950
    if ax is None:
        ax = plt.gca()
    ax.set_ylabel(ylabel_text, ha="left", rotation=0, gid="rws-ylabel", **kwargs)

    # Put in the top left corner above graph
    fig = ax.get_figure()
    ax_height_inches = (
        ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).height
    )
    ax.yaxis.set_label_coords(0, 1 + 1 / inches_to_points(ax_height_inches))


def source(text: str, fig: plt.Figure = None, **kwargs) -> None:
    """Add a source with formatting.

    Adds a source below the graph. The source is placed in the bottom left.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.source('My source')
    >>> rlt.show()
    ERROR:2023/09/06 14:25:23 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:25:23 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:25:23 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:25:23 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:25:23 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    text
        The source to be added. It will be shown as "Bron: {source}"
    fig
        The figure to place the source in, default plt.gcf().
    **kwargs
        Keyword arguments will be passed to matplotlib.pyplot.figtext
    """  # noqa: B950
    if not fig:
        fig = plt.gcf()

    text = f"Bron: {text}"

    fontsize = "small"
    lineheight_inches = points_to_inches(get_fontsize_points(fontsize))
    padding_inches = lineheight_inches
    lineheight_fraction = lineheight_inches / fig.get_figheight()

    color = plt.rcParams["axes.labelcolor"]

    figtext(
        text,
        color,
        y=lineheight_fraction,
        lineheight_inches=lineheight_inches,
        fontsize=fontsize,
        gid="rws-source",
        fig=fig,
        **kwargs,
    )

    increase_bottom_margin(lineheight_inches + padding_inches, fig)

    # adjust position of logo
    fig = plt.gcf()
    size = fig.get_size_inches()
    logo_figtexts = [text for text in fig.texts if text.get_gid() == "rws-logo"]

    for logo_figtext in logo_figtexts:
        old_position = logo_figtext.get_position()
        logo_figtext.set_position(
            [
                old_position[0],
                old_position[1] + ((lineheight_inches + padding_inches)) / size[1],
            ]
        )


def logo(
    text: str = "logo",
    offset_x: float = 0,
    offset_y: float = 0,
    fig: plt.Figure = None,
) -> None:
    """Add logo with formatting.

    Adds a textual logo to the right of the graph. The logo is placed in the
    bottom right corner of the graph.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.logo('My department name')
    >>> rlt.show()
    ERROR:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')

    Parameters
    ----------
    text:
        The text to be added as logo.
    offset_x, optional
        Offset in points, in x-direction (positive right), by default 0
    offset_y, optional
        Offset in points, in y-direction (positive up), by default 0
    fig
        The figure to place the logo in, default plt.gcf().
    """  # noqa: B950
    if not fig:
        fig = plt.gcf()
    coordinate_system = fig.transFigure

    fontsize = "x-small"
    lineheight_inches = points_to_inches(get_lineheight_points(fontsize))

    padding_inches = points_to_inches(4)
    horizontal_space_needed_inches = lineheight_inches + padding_inches

    if 1 - get_right_margin(fig) < horizontal_space_needed_inches / fig.get_figwidth():
        increase_right_margin(horizontal_space_needed_inches, fig)

    x = (
        get_right_margin(fig)
        + (padding_inches + points_to_inches(offset_x)) / fig.get_figwidth()
    )
    y = (
        get_bottom_margin(fig)
        + (padding_inches + points_to_inches(offset_y)) / fig.get_figwidth()
    )

    plt.figtext(
        x=x,
        y=y,
        s=text,
        fontsize=fontsize,
        color=rijkskleuren["grijs-7"],
        ha="left",
        va="bottom",
        rotation="vertical",
        transform=coordinate_system,
        figure=fig,
        gid="rws-logo",
    )


def logo_rwsdatalab(fig: plt.Figure = None, **kwargs) -> None:
    """Add RWS Datalab logo to right of graph.

    Adds a text version of the RWS Datalab logo to the right of the graph.
    The logo is placed in the bottom right corner of the graph.

    .. warning:: This function is only intended for members of the RWS Datalab.
        If you are not a member of the RWS Datalab team, please use
        :func:`rijksplotlib.pyplot.logo` instead.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3])
    >>> rlt.logo_rwsdatalab()
    >>> rlt.show()
    ERROR:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:26:18 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')

    Parameters
    ----------
    fig
        The figure to place the RWS datalab logo in, default plt.gcf().
    kwargs
        Optional keyword arguments are passed to `rlt.logo()`
    """  # noqa: B950
    if not fig:
        fig = plt.gcf()
    text = "RWS Datalab"
    logo(text, fig=fig, **kwargs)


def legend(
    padding_right_inches: float = 0.7,
    fig: plt.Figure = None,
    ax: matplotlib.axes.Axes = None,
    *args,
    **kwargs,
) -> None:
    """Make legend on upper right of figure.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([1, 2, 3], label='My line')
    >>> rlt.legend()
    >>> rlt.show()
    ERROR:2023/09/06 14:32:22 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:32:22 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:32:22 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    WARNING:2023/09/06 14:32:22 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:32:22 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    padding_right_inches
        the number of inches to make room for the legend
    fig
        The figure to place the legend in, default plt.gcf().
    ax
        Optional, the matplotlib Axes to put a legend in. If not given,
        the current active Axes will be picked.
    kwargs
        kwargs to pass along to ax.legend
    """  # noqa: B950
    if not fig:
        fig = plt.gcf()
    figwidth = fig.get_figwidth()
    padding_right_ratio = padding_right_inches / figwidth
    fig.subplots_adjust(right=1 - padding_right_ratio)

    # make legend
    if ax is None:
        ax = plt.gca()
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1, 1),
        handleheight=1.3,
        handlelength=1.8,
        labelspacing=0.4,
        *args,
        **kwargs,
    )

    # adjust position of logo
    logo_figtexts = [text for text in fig.texts if text.get_gid() == "rws-logo"]
    for logo_figtext in logo_figtexts:
        old_position = logo_figtext.get_position()
        logo_figtext.set_position(
            [2 - old_position[0] - padding_right_ratio, old_position[1]]
        )


def _axhline_zero(ax: matplotlib.axes.Axes = None, **kwargs) -> None:
    """Plot horizontal line at y=0 with spine styling.

    Creates a horizontal line at y=0 with the same styling as the spine.
    This is meant to accentuate the zero line.

    .. warning:: This function is not meant to be used directly. Use
        :func:`rijksplotlib.pyplot.set_spine_zero` instead.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([-3, -2, -1, 0, 1, 2, 3])
    >>> rlt._axhline_zero()
    >>> rlt.show()
    ERROR:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    ax
        Optional, the matplotlib Axes to put a line in. If not given,
        the current active Axes will be picked.
    kwargs
        kwargs are passed to ax.axhline
    """  # noqa: B950
    if ax is None:
        ax = plt.gca()
    linecolor = plt.rcParams["axes.edgecolor"]
    linewidth = plt.rcParams["axes.linewidth"]
    ax.axhline(y=0, color=linecolor, linewidth=linewidth, zorder=0, **kwargs)


def _axvline_zero(ax: matplotlib.axes.Axes = None, **kwargs) -> None:
    """Plot vertical line at x=0 with spine styling.

    Creates a vertical line at x=0 with the same styling as the spine.

    .. warning:: This function is not meant to be used directly. Use
        :func:`rijksplotlib.pyplot.set_spine_zero` instead. With the
        ``axis='vertical'`` option.

    Parameters
    ----------
    ax
        Optional, the matplotlib Axes to put a line in. If not given,
        the current active Axes will be picked.
    kwargs
        kwargs are passed to ax.axhline
    """
    if ax is None:
        ax = plt.gca()
    linecolor = plt.rcParams["axes.edgecolor"]
    linewidth = plt.rcParams["axes.linewidth"]
    ax.axvline(x=0, color=linecolor, linewidth=linewidth, zorder=0, **kwargs)


def set_spine_zero(
    axis="horizontal", ax: matplotlib.axes.Axes = None, **kwargs
) -> None:
    """Plot spine at zero instead of axis edge.

    Sets axhline and/or axvline at zero and remove axis spine(s).

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import rijksplotlib.pyplot as rlt
    >>> plt.plot([-3, -2, -1, 0, 1, 2, 3])
    >>> rlt.set_spine_zero()
    >>> rlt.show()
    ERROR:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a title, use rlt.title('your title')
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing xlabel, is this correct? If not, use rlt.xlabel('your xlabel').
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing ylabel, is this correct? If not, use rlt.ylabel('your ylabel').
    INFO:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing legend, is this correct? If not, use rlt.legend()
    WARNING:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a source, use rlt.source('your source')
    WARNING:2023/09/06 14:33:48 PM - rijksplotlib.validate - Missing a department logo, use rlt.logo_rwsdatalab() or rlt.logo('My department name')

    Parameters
    ----------
    axis : {'both', 'horizontal', 'vertical'}, optional
        Which axis to use when setting spine to zero, by default "horizontal"
    ax
        Optional, the matplotlib Axes to put a line in. If not given,
        the current active Axes will be picked.
    kwargs
    """  # noqa: B950
    mpl._api.check_in_list(["horizontal", "vertical", "both"], axis=axis)
    if ax is None:
        ax = plt.gca()
    ax.grid(
        axis="y", clip_on=False
    )  # Make sure the grid line at the axes edges is not clipped off
    if axis in ["horizontal", "both"]:
        _axhline_zero(**kwargs)
        ax.spines["bottom"].set_visible(False)
    if axis in ["vertical", "both"]:
        _axvline_zero(**kwargs)
        ax.spines["left"].set_visible(False)
