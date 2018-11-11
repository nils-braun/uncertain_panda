uncertain_panda
===============

.. image:: https://badge.fury.io/py/uncertain_panda.svg
           :target: https://badge.fury.io/py/uncertain_panda
.. image:: https://coveralls.io/repos/github/nils-braun/uncertain_panda/badge.svg?branch=master
           :target: https://coveralls.io/github/nils-braun/uncertain_panda?branch=master
.. image:: https://travis-ci.org/nils-braun/uncertain_panda.svg?branch=master
           :target: https://travis-ci.org/nils-braun/uncertain_panda


``uncertain_panda`` helps you with constructing uncertainties of quantities calculated on your ``pandas`` data frames,
by applying the method of bootstrapping.


Why is the panda uncertain?
---------------------------

Have you ever calculated quantities on your pandas data frame/series and wanted to know their uncertainty?
Did you ever wondered if the difference in the average of two methods is significant?

Then you want to have an uncertain panda!

``uncertain_panda`` helps you calculate uncertainties on arbitrary quantities related to your pandas data frame
e.g. ``mean``, ``median``, ``quantile`` or ``min``/``max`` and every other arbitrary function on pandas data frames!


How to use it?
--------------

First, install the package

.. code-block:: bash

    pip install uncertain_panda

Just import pandas from the ``uncertain_panda`` package and prefix ``unc`` before every calculation.

.. code-block:: python

    from uncertain_panda import pandas as pd

    series = pd.Series([1, 2, 3, 4, 5, 6, 7])
    series.unc.mean()

That's it!
The return value is an instance of the uncertainty value from the superb `uncertainties`_ package.
As this package already knows how to calculate with uncertainties, you can use the
results as they were normal numbers in your calculations.
Super easy!


.. _`uncertainties`: https://pythonhosted.org/uncertainties/


Features
--------

The development has just started and there is a lot that can still be added.
Here is a list of already implemented features

*   Automatic calculation of uncertainties of every built in pandas function for

    * data frames
    * series
    * grouped data frames

    using the prefix ``unc`` before the function name, e.g.

    .. code-block:: python

        df.unc.mean()

    In the background, it used the method of bootstrapping (see below) to calculate
    the uncertainties.

*   Possibility to calculate asymmetric or symmetric uncertainties, with ``unc`` or ``unc_asym``.
*   Plotting functionality for uncertainties with

    .. code-block:: python

        df.unc.mean().plot_with_uncertainties(kind="bar")

    for a nice error-bar plot.
*   Full configurable bootstrapping with either using pandas built-in methods or ``dask`` (optionally enabled).
    Just pass the options to your called method, e.g.

    .. code-block:: python

        df.unc.mean(pandas=False)

    to use ``dask`` instead of pandas for the bootstrapping.


How does it work?
-----------------

Under the hood, ``uncertain_panda`` is using bootstrapping for calculating the uncertainties.
Supose you want to calculate a quantity :math:`f(X)` on your data frame :math:`X`.
Bootstrapping samples multiple versions :math:`Y_i` of :math:`X` by drawing elements with replacement from the
data frame with the same length the data frame itself.
On all these :math:`Y_i`, the function :math:`f` is evaluated, creating a distribution of possible values for
:math:`f(X)`.
The standard deviation of this distribution is the (symmetric) uncertainty returned by ``uncertain_panda``.
If you request the asymmetric uncertainty, the 1 sigma quantile in both directions around the median
is returned.
You can find some more information on bootstrapping in the net, e.g. on wikipedia_.

.. _`wikipedia`: `https://en.wikipedia.org/wiki/Bootstrapping_(statistics)`