############
rijksplotlib
############

.. begin-inclusion-intro-marker-do-not-remove

A datavizualization compliance library for RWS Datalab

The goal of this package is to easily transform your standard `matplotlib` figures (left) to better, recognizable and accessible ones (right).

|pic_mpl|   |pic_rpl|

.. |pic_mpl| image:: https://gitlab.com/rwsdatalab/public/codebase/tools/rijksplotlib/-/raw/main/doc/static/images/startpagina_1_matplotlib.png
  :alt: A screenshot of an RWS report with a default matplotlib plot. The styling of the matplotlib plot does not match the styling of the document.
  :width: 350px

.. |pic_rpl| image:: https://gitlab.com/rwsdatalab/public/codebase/tools/rijksplotlib/-/raw/main/doc/static/images/startpagina_3_import_rijksplotlib_and_use_helper_functions.png
  :alt: The same screenshot of an RWS report, but with a plot styled using the Rijksplotlib package and helper functions. The figure matches the styling of the document.
  :width: 350px

With just a few lines of code, the text in the figure is aligned with the text in an RWS report and the graph dimensions are optimized. Furthermore, the colors and other styling elements are updated to conform to the Rijkshuisstijl and RWS huisstijl.

.. end-inclusion-intro-marker-do-not-remove


.. begin-inclusion-installation-marker-do-not-remove

Installation
------------
To install the ``rijksplotlib`` package, you need to have Python 3.10
or higher installed.

.. code-block:: bash

  pip install rijksplotlib

Want to install the Pylint rules included in rijksplotlib in your CI/CD pipeline?
Have a look at the `CI/CD setup guide <https://rwsdatalab.gitlab.io/public/codebase/tools/rijksplotlib/linter.html#gitlab-ci-integration>`_.

Installing from source
^^^^^^^^^^^^^^^^^^^^^^
If you want to work on the ``rijksplotlib`` codebase, you'll probably want to install from source.
Or if you simply want to try out the latest features before they are released.
To install rijksplotlib from source, run this command in your terminal:

.. code-block:: bash

  git clone https://gitlab.com/rwsdatalab/public/codebase/tools/rijksplotlib.git
  cd rijksplotlib
  pip install .

Run tests (including coverage) with:

.. code-block:: bash

  pip install ".[dev]"
  pytest

Documentation and examples can be generated with:

.. code-block:: bash

  pip install ".[doc]"
  make --directory=doc html # if using Windows use .\doc\make.bat html

.. warning ::

  The documentation dependencies require ``pydantic < 2.0.0``, which is incompatible with the latest version of ``rijksplotlib``.
  Therefore, after installing the documentation dependencies, you need to upgrade ``pydantic`` to the latest 2.x version.


.. end-inclusion-installation-marker-do-not-remove

.. begin-inclusion-usage-marker-do-not-remove

Getting started
---------------

Plot your figure in the way you are used to. Then, use ``rlt.show()`` or ``rlt.savefig`` instead of using ``plt.show()`` or ``plt.savefig()`` to show or save the figure.

.. code-block:: python

    import rijksplotlib.pyplot as rlt

    # plot your graph here #

    rlt.show()
    # or #
    rlt.savefig()


This package helps you optimize your figures for RWS reports. Using the ``rijksplotlib.pyplot.show`` or ``rijksplotlib.pyplot.savefig`` helper functions, it provides feedback when you are missing elements necessary for a good figure. Furthermore, the resulting figure fits precisely within the RWS report preset margins. When you place your figure in a report, the font sizes of all elements are readable and fit in with the rest of the text well.

For more background information on making representative and good figures, see the `Stijlgids Datavisualisatie RWS <https://pleinienw.nl/articles/297813>`_ (intranet).

.. end-inclusion-usage-marker-do-not-remove

.. begin-inclusion-license-marker-do-not-remove

License
-------

.. code-block:: text

   Copyright 2023 Rijkswaterstaat

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

.. end-inclusion-license-marker-do-not-remove
