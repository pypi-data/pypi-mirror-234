# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

from ._version import __version__

from .thinning import (
    SteinThinning,
    RegularizedSteinThinning
)

from .discrepancies import (
    MMD,
    KSD
)

from .bjsamplers import (
    rmh,
    hmc,
    nuts,
    mala
)

from .utils import (
    laplace_log_p_hardplus,
    laplace_log_p_softplus
)

__all__ = ["__version__",
           "SteinThinning",
           "RegularizedSteinThinning",
           "laplace_log_p_hardplus",
           "laplace_log_p_softplus",
           "MMD",
           "KSD",
           "rmh",
           "hmc",
           "nuts",
           "mala"]