uncertain_panda
===============

``uncertain_panda`` helps you with constructing uncertainties of quantities calculated on your ``pandas`` data frames,
by applying the method of bootstrapping.

.. image:: https://readthedocs.org/projects/uncertain-panda/badge/?version=latest&style=flat-sphare
           :target: https://uncertain-panda.readthedocs.io/en/stable/
.. image:: https://badge.fury.io/py/uncertain_panda.svg
           :target: https://badge.fury.io/py/uncertain_panda
.. image:: https://coveralls.io/repos/github/nils-braun/uncertain_panda/badge.svg?branch=master
           :target: https://coveralls.io/github/nils-braun/uncertain_panda?branch=master
.. image:: https://travis-ci.org/nils-braun/uncertain_panda.svg?branch=master
           :target: https://travis-ci.org/nils-braun/uncertain_panda


Why is the panda uncertain?
---------------------------

Have you ever calculated quantities on your pandas data frame/series and wanted to know their uncertainty?
Did you ever wondered if the difference in the average of two methods is significant?

Then you want to have an uncertain panda!

``uncertain_panda`` helps you calculate uncertainties on arbitrary quantities related to your pandas data frame
e.g. ``mean``, ``median``, ``quantile`` or ``min``/``max`` and every other arbitrary function on pandas data frames!

You can use any measured data (e.g. from A/B testing, recorded data from an experiment or any type of tabular data)
and calculate any quantity using ``pandas`` and ``uncertain_panda`` will give you the uncertainty on this quantity.


How to use it?
--------------

First, install the package

.. code-block:: bash

    pip install uncertain_panda

Now, just import pandas from the ``uncertain_panda`` package and prefix ``unc`` before every calculation
to get the value with the uncertainty:

.. code-block:: python

    from uncertain_panda import pandas as pd

    series = pd.Series([1, 2, 3, 4, 5, 6, 7])
    series.unc.mean()

That's it!
The return value is an instance of the uncertainty ``Variable`` from the superb `uncertainties`_ package.
As this package already knows how to calculate with uncertainties, you can use the
results as if they were normal numbers in your calculations.


.. code-block:: python

    series.unc.mean() + 2 * series.unc.std()

Super easy!

You can find some more examples in :ref:`examples`.

Comparison in A/B testing
.........................

Suppose you have done some A/B testing with a brand new feature you want to introduce.
You have measured the quality of your service before (*A*) and after (*B*) the feature introduction.
The averge quality is better, but is the change significant?

A first measure for this problem might be the uncertainty of the average, so lets calculate it:

.. code-block:: python

    data_frame.groupby("feature_introduced").quality.unc.mean()

which will not only give you the two average qualities but also their uncertainties.

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

*   Calculate confidence intervals (instead of symmetric one-sigma uncertainties)
    or get back the basic bootstrapping distribution with

    .. code-block:: python

      df.unc.mean().bs()  # for the bootstrap distribution
      df.unc.mean().ci(0.3, 0.7)  # for the confidence interval between 0.3 and 0.7

*   Opional usage of ``dask`` for large data samples.
    Enable it with

    .. code-block:: python

        df.unc.mean(pandas=False)

    to use ``dask`` instead of pandas.

*   Plotting functionality for uncertainties with

    .. code-block:: python

        df.unc.mean().plot_with_uncertainty(kind="bar")

    for a nice error-bar plot.
*   Full configurable bootstrapping.
    Just pass the options to your called method, e.g.

    .. code-block:: python

        df.unc.mean(number_of_draws=300)

    to use 300 draws in the bootstrapping.


How does it work?
-----------------

Under the hood, ``uncertain_panda`` is using bootstrapping for calculating the uncertainties.
Find more information on bootstrapping in :ref:`bootstrapping`.

Other packages
--------------

There are probably plenty of packages out there for this job, that I am not aware of.
The best known is probably the `bootstrapped`_ package.
Compared to this package, ``uncertain_panda`` tries to automate the quantity calculation
and works for arbitrary functions.
Also, it can use ``dask`` for the calculation.
``bootstrapped`` on the other hand is very nice for sparse arrays, which is not (yet) implemented in
``uncertain_panda``.

.. _`bootstrapped`: https://github.com/facebookincubator/bootstrapped
