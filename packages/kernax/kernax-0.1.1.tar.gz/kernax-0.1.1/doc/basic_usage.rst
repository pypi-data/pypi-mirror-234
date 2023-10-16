Basic usage
===========

We briefly show how to use to two main functions of this package. Let's say that we want to thin a Gaussian sample with Stein thinning and regularized Stein thinning, and that
the target distribution is also Gaussian.

First generate a toy sample.

.. code::

    import numpy as np
    x = np.random.randn(1000,2)

In order to apply Stein thinning, we need the values of the score function and a lengthscale. 
Here, the expression of the target score function is straightforward and can be implemented by hand or with, e.g., scipy.

.. code::

    from jax.scipy.stats import multivariate_normal    
    score_fn = multivariate_normal.logpdf
    score_values = jax.vmap(score_fn, 0)(x)

We also need a lengthscale which is chosen as the median heuristic.

.. code::
    
    from kernax.utils import median_heuristic
    lengthscale = median_heuristic(x)

Stein thinning can applied as follows to select 100 points amongst the original sample.

.. code::

    from kernax import SteinThinning
    stein_fn = SteinThinning(x, score_values, lengthscale)
    indices = stein_fn(100)

Regularized Stein thinning can be used in a similar fashion but requires an additional input, the expression of the Laplace correction.

.. code::

    from kernax import laplace_log_p_softplus
    laplace_log_p_values = laplace_log_p_softplus(x, score_fn)

    from kernax import RegularizedSteinThinning
    reg_stein_fn = RegularizedSteinThinning(x, score_values, laplace_log_p_values, lengthscale)
    indices = reg_stein_fn(100)

Additional comments or examples can be found in the API documentation.