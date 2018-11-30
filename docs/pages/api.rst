.. _`api`:

API
===

First things first
------------------

If you want to use ``uncertain_panda``, you need to call the following line at the beginning of your script/notebook:

.. code-block:: python

    from uncertain_panda import pandas as pd

This will load ``pandas`` as normal, but will add the uncertainty calculations described in the following.
It is basically equivalent to do

.. code-block:: python

    import pandas as pd

and then add the additional features of ``uncertain_panda`` by hand.


Calculating a quantity with uncertainty
---------------------------------------

In the following, lets suppose you have a pandas object (could be a ``pandas.Series``, a ``pandas.DataFrame`` or
even the result of a ``groupby`` operation) which we call ``df``.
You want to calculate a function ``f`` on them and normally you would call

.. code-block:: python

    df.f()

or with arguments

.. code-block:: python

    df.f(some_arg=value)

To do the same calculation, but this time with uncertainties, just add an `unc` in between:

.. code-block:: python

    df.unc.f()
    df.unc.f(some_arg=value)

The return value is a number/series/data frame (whatever ``f`` normally returns) with uncertainties.
Thanks to the `uncertainties`_ package (make sure to star this great package),
these results behave just as normal numbers.
The error is even propagated correctly!
Remember, ``df`` can be any pandas object and ``f`` can be any pandas function, so you can do things like

.. code-block:: python

    df.groupby("group").unc.median()
    df[df.x > 3].y.unc.quantile(0.25)
    (df + 2).loc["A"].unc.sum()

The results will behave as the normal function call - just with the uncertainties added!


Advanced functionality
----------------------

Actually, the return values of the uncertainty calculations are not only "bare numbers with uncertainties".
They have a bunch of additional functionality:

.. py:currentmodule:: uncertain_panda
.. autoclass:: BootstrapResult


Plotting
--------


.. _`uncertainties`: https://pythonhosted.org/uncertainties/