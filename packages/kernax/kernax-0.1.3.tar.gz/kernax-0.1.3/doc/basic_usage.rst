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

    def logprob_fn(x):
        return multivariate_normal(x, mean=jnp.zeros(2), cov=jnp.eye(2))

    score_fn = jax.grad(logprob_fn)
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

Regularized Stein thinning can be used in a similar fashion but requires two additional inputs: the log-probability values,
and the regularization terms.

.. code::

    from kernax import laplace_log_p_softplus
    log_p_values = jax.vmap(logprob_fn, 0)(x)
    laplace_log_p_values = laplace_log_p_softplus(x, score_fn)

    from kernax import RegularizedSteinThinning
    reg_stein_fn = RegularizedSteinThinning(x, log_p_values, score_values, laplace_log_p_values, lengthscale)
    indices = reg_stein_fn(100)

Additional comments or examples can be found in the API documentation.