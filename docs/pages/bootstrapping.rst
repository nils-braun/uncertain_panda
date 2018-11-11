.. _`bootstrapping`:

Bootstrapping
=============

Suppose you want to calculate a quantity :math:`f(X)` on your data frame :math:`X`.
Bootstrapping samples multiple versions :math:`Y_i` of :math:`X` by drawing elements with replacement from the
data frame with the same length the data frame itself.
On all these :math:`Y_i`, the function :math:`f` is evaluated, creating a distribution of possible values for
:math:`f(X)`.
The standard deviation of this distribution is the (symmetric) uncertainty returned by ``uncertain_panda``.
If you request the asymmetric uncertainty, the 1 sigma quantile in both directions around the median
is returned.
You can find some more information on bootstrapping in the net, e.g. on wikipedia_.

.. _`wikipedia`: `https://en.wikipedia.org/wiki/Bootstrapping_(statistics)`