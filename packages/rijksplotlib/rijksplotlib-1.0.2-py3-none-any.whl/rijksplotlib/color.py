"""A dictionary of colors that can be used in the rijksplotlib library.

The ``rijksplotlib.color.rijkskleuren`` dictionary contains all colors that can
be used in the rijksplotlib library. The colors are from the `Rijkshuisstijl color palette
<https://www.rijkshuisstijl.nl/publiek/modules/product/DigitalStyleGuide/default/index.aspx?ItemId=6744>`_.
The colors are defined as hex values.

One can use the colors in the dictionary as follows:

.. code-block:: python

    from rijksplotlib.color import rijkskleuren
    rijkskleuren["logoblauw"]  # returns "#154273"
    rijkskleuren["grijs-1"]  # returns "#f3f3f3"
    rijkskleuren["donkergeel-tint-4"]  # returns "#FEE9B7"
    # ...

An overview of all colors in the dictionary can be found in the
:ref:`sphx_glr_auto_examples_colors_plot_preview_color.py`

.. image:: /auto_examples/colors/images/sphx_glr_plot_preview_color_001.png
  :alt: All colors available within the package.

"""

general = {"wit": "#fff", "zwart": "#000"}

grijs = {
    "grijs-1": "#f3f3f3",
    "grijs-2": "#e6e6e6",
    "grijs-3": "#cccccc",
    "grijs-4": "#b4b4b4",
    "grijs-5": "#999999",
    "grijs-6": "#696969",
    "grijs-7": "#535353",
}

logoblauw = {
    "logoblauw": "#154273",
    "logoblauw-tint-1": "#4f7196",
    "logoblauw-tint-2": "#738eab",
    "logoblauw-tint-3": "#95a9c0",
    "logoblauw-tint-4": "#b8c6d5",
    "logoblauw-tint-5": "#dce3ea",
}

lichtblauw = {
    "lichtblauw": "#8fcae7",
    "lichtblauw-tint-1": "#ABD7ED",
    "lichtblauw-tint-2": "#BCDFF0",
    "lichtblauw-tint-3": "#CCE7F4",
    "lichtblauw-tint-4": "#DDEFF8",
    "lichtblauw-tint-5": "#EEF7FC",
}

hemelblauw = {
    "hemelblauw": "#007bc7",
    "hemelblauw-tint-1": "#409CD5",
    "hemelblauw-tint-2": "#66AFDD",
    "hemelblauw-tint-3": "#8CC3E6",
    "hemelblauw-tint-4": "#B2D7EE",
    "hemelblauw-tint-5": "#D9EBF7",
}

donkerblauw = {
    "donkerblauw": "#01689b",
    "donkerblauw-tint-1": "#408EB4",
    "donkerblauw-tint-2": "#66A4C3",
    "donkerblauw-tint-3": "#8CBBD2",
    "donkerblauw-tint-4": "#B2D1E1",
    "donkerblauw-tint-5": "#D9E8F0",
}

mintgroen = {
    "mintgroen": "#72d2b6",
    "mintgroen-tint-1": "#98DDC8",
    "mintgroen-tint-2": "#ACE4D3",
    "mintgroen-tint-3": "#C1EBDE",
    "mintgroen-tint-4": "#D5F1E9",
    "mintgroen-tint-5": "#EAF8F4",
}

mosgroen = {
    "mosgroen": "#777B00",
    "mosgroen-tint-1": "#999C40",
    "mosgroen-tint-2": "#ADAF66",
    "mosgroen-tint-3": "#C1C38C",
    "mosgroen-tint-4": "#D6D7B2",
    "mosgroen-tint-5": "#EBEBD9",
}

groen = {
    "groen": "#39870C",
    "groen-tint-1": "#6AA549",
    "groen-tint-2": "#88B76D",
    "groen-tint-3": "#A5C991",
    "groen-tint-4": "#C3DBB5",
    "groen-tint-5": "#E1EDDA",
}

donkergroen = {
    "donkergroen": "#275937",
    "donkergroen-tint-1": "#5D8269",
    "donkergroen-tint-2": "#7D9B87",
    "donkergroen-tint-3": "#9DB4A4",
    "donkergroen-tint-4": "#BDCDC2",
    "donkergroen-tint-5": "#DEE6E1",
}

bruin = {
    "bruin": "#94710A",
    "bruin-tint-1": "#AF9447",
    "bruin-tint-2": "#BFA96C",
    "bruin-tint-3": "#CFBF90",
    "bruin-tint-4": "#DFD4B5",
    "bruin-tint-5": "#EFEADA",
}

donkerbruin = {
    "donkerbruin": "#673327",
    "donkerbruin-tint-1": "#8D665D",
    "donkerbruin-tint-2": "#A3847D",
    "donkerbruin-tint-3": "#BAA39D",
    "donkerbruin-tint-4": "#D1C1BD",
    "donkerbruin-tint-5": "#E8E0DF",
}

geel = {
    "geel": "#F9E11E",
    "geel-tint-1": "#FAE856",
    "geel-tint-2": "#FBED78",
    "geel-tint-3": "#FCF199",
    "geel-tint-4": "#FDF6BB",
    "geel-tint-5": "#FEFBDD",
}

donkergeel = {
    "donkergeel": "#FFB612",
    "donkergeel-tint-1": "#FDC84D",
    "donkergeel-tint-2": "#FDD370",
    "donkergeel-tint-3": "#FDDE94",
    "donkergeel-tint-4": "#FEE9B7",
    "donkergeel-tint-5": "#FEF4DB",
}

oranje = {
    "oranje": "#E17000",
    "oranje-tint-1": "#E89440",
    "oranje-tint-2": "#EDA966",
    "oranje-tint-3": "#F1BE8C",
    "oranje-tint-4": "#F6D4B2",
    "oranje-tint-5": "#FBEAD9",
}

rood = {
    "rood": "#D52B1E",
    "rood-tint-1": "#DF6056",
    "rood-tint-2": "#E67F78",
    "rood-tint-3": "#EC9F99",
    "rood-tint-4": "#F2BFBB",
    "rood-tint-5": "#F9DFDD",
}

roze = {
    "roze": "#F092CD",
    "roze-tint-1": "#F4ADD9",
    "roze-tint-2": "#F6BDE1",
    "roze-tint-3": "#F8CEE8",
    "roze-tint-4": "#FBDEF0",
    "roze-tint-5": "#FDEFF8",
}

robijnrood = {
    "robijnrood": "#CA005D",
    "robijnrood-tint-1": "#D74085",
    "robijnrood-tint-2": "#DF669D",
    "robijnrood-tint-3": "#E78CB6",
    "robijnrood-tint-4": "#EFB2CE",
    "robijnrood-tint-5": "#F7D9E7",
}

violet = {
    "violet": "#a90061",
    "violet-tint-1": "#BE4088",
    "violet-tint-2": "#CB66A0",
    "violet-tint-3": "#D88CB7",
    "violet-tint-4": "#E5B2CF",
    "violet-tint-5": "#F2D9E7",
}

paars = {
    "paars": "#42145F",
    "paars-tint-1": "#714F87",
    "paars-tint-2": "#8D729F",
    "paars-tint-3": "#A995B7",
    "paars-tint-4": "#C6B8CE",
    "paars-tint-5": "#E3DCE7",
}


rijkskleuren = {
    **general,
    **grijs,
    **logoblauw,
    **lichtblauw,
    **hemelblauw,
    **donkerblauw,
    **mintgroen,
    **mosgroen,
    **groen,
    **donkergroen,
    **bruin,
    **donkerbruin,
    **geel,
    **donkergeel,
    **oranje,
    **rood,
    **roze,
    **robijnrood,
    **violet,
    **paars,
}
