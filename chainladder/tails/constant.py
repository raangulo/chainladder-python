"""
:ref:`chainladder.tails<tails>`.Constant
=========================================

:ref:`TailConstant<constant>` is a constant.
"""

from chainladder.tails import TailBase
from chainladder.development import DevelopmentBase

class TailConstant(TailBase):
    """Allows for the entry of a constant tail factor to LDFs.

    Parameters
    ----------
    tail : float
        The constant to apply to all LDFs within a triangle object.

    Attributes
    ----------
    ldf_ :
        ldf with tail applied.
    cdf_ :
        cdf with tail applied.
    sigma_ :
        sigma with tail factor applied.
    std_err_ :
        std_err with tail factor applied

    Examples
    --------
    >>> import chainladder as cl
    >>> abc = cl.Development().fit_transform(cl.load_dataset('abc'))
    >>> abc = cl.TailConstant(tail=1.05).fit_transform(abc)
    >>> abc.ldf_
             12-24     24-36     36-48     48-60     60-72     72-84     84-96    96-108   108-120   120-132  132-Ult
    1977  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1978  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1979  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1980  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1981  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1982  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1983  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1984  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1985  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1986  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05
    1987  2.308599  1.421098  1.199934  1.113445  1.072736  1.047559  1.034211  1.026047  1.020188  1.016259     1.05

    Notes
    -----
    The tail constant does not support the entry of variability parameters
    necessary for stochastic approaches, so any usage of TailConstant will be
    inherently deterministic.

    See also
    --------
    TailCurve

    """
    def __init__(self, tail=1.0):
        self.tail = tail

    def fit(self, X, y=None, sample_weight=None):
        """Fit the model with X.

        Parameters
        ----------
        X : Triangle-like
            Set of LDFs to which the tail will be applied.
        y : Ignored
        sample_weight : Ignored

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        super().fit(X, y, sample_weight)
        self.ldf_.values[..., -1] = self.ldf_.values[..., -1]*self.tail
        self.cdf_ = DevelopmentBase._get_cdf(self)
        return self

    def transform(self, X):
        """Transform X.
        The predicted class of an input sample is a vote by the trees in
        the forest, weighted by their probability estimates. That is,
        the predicted class is the one with highest mean probability
        estimate across the trees.

        Parameters
        ----------
        X : Triangle
            Triangle must contain the ``ldf_`` development attribute.

        Returns
        -------
        X_new : Triangle
            New Triangle with tail factor applied to its development
            attributes.
        """
        X.std_err_ = self.std_err_
        X.cdf_ = self.cdf_
        X.ldf_ = self.ldf_
        X.sigma_ = self.sigma_
        return X
