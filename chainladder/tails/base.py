import copy
import numpy as np
from sklearn.base import BaseEstimator
from chainladder.development import DevelopmentBase, Development


class TailBase(BaseEstimator):
    ''' Base class for all tail methods.  Tail objects are equivalent
        to development objects with an additional set of tail statistics'''

    def __init__(self):
        pass

    def fit(self, X, y=None, sample_weight=None):
        obj = copy.deepcopy(X)
        if obj.__dict__.get('ldf_', None) is None:
            obj = Development().fit_transform(obj)
        self._ave_period = {'Y': (1, 12), 'Q': (4, 3), 'M': (12, 1)}[obj.development_grain]
        ddims = np.concatenate(
            (obj.ddims, [(item+1)*self._ave_period[1] + obj.ddims[-1]
                       for item in range(self._ave_period[0])], [9999]), 0)
        self.ldf_ = copy.deepcopy(obj.ldf_)
        tail = np.ones(self.ldf_.shape)[..., -1:]
        tail = np.repeat(tail, self._ave_period[0]+1, -1)
        self.ldf_.values = np.concatenate((self.ldf_.values, tail), -1)
        self.ldf_.ddims = np.array(['{}-{}'.format(ddims[i], ddims[i+1])
                                    for i in range(len(ddims)-1)])
        self.ldf_.valuation = self.ldf_._valuation_triangle()
        self.sigma_ = copy.deepcopy(obj.__dict__.get('sigma_', obj.cdf_*0))
        self.std_err_ = copy.deepcopy(obj.__dict__.get('std_err_', obj.cdf_*0))
        zeros = tail[..., -1:]*0
        self.sigma_.values = np.concatenate(
            (self.sigma_.values, zeros), -1)
        self.std_err_.values = np.concatenate(
            (self.std_err_.values, zeros), -1)
        self.sigma_.ddims = self.std_err_.ddims = \
            np.append(obj.ldf_.ddims, ['{}-9999'.format(int(obj.ddims[-1]))])
        val_array = self.sigma_._valuation_triangle(self.sigma_.ddims)
        self.sigma_.valuation = self.std_err_.valuation = val_array
        self.cdf_ = DevelopmentBase._get_cdf(self)
        return self

    def transform(self, X):
        X_new = copy.deepcopy(X)
        X_new.std_err_.values = np.concatenate(
            (X_new.std_err_.values,
             self.std_err_.values[..., -1:]), -1)
        X_new.cdf_.values = np.concatenate(
            (X_new.cdf_.values,
             self.cdf_.values[..., -self._ave_period[0]-1:]*0+1), -1)
        X_new.cdf_.values = X_new.cdf_.values * \
            self.cdf_.values[..., -self._ave_period[0]-1:-self._ave_period[0]]
        X_new.cdf_.values[..., -1] = self.cdf_.values[..., -1]
        X_new.ldf_.values = np.concatenate(
            (X_new.ldf_.values,
             self.ldf_.values[..., -self._ave_period[0]-1:]), -1)
        X_new.sigma_.values = np.concatenate(
            (X_new.sigma_.values, self.sigma_.values[..., -1:]), -1)
        X_new.cdf_.ddims = X_new.ldf_.ddims = self.ldf_.ddims
        X_new.sigma_.ddims = X_new.std_err_.ddims = self.sigma_.ddims
        X_new.cdf_.valuation = X_new.ldf_.valuation = self.ldf_.valuation
        X_new.sigma_.valuation = X_new.std_err_.valuation = self.sigma_.valuation
        return X_new

    def fit_transform(self, X, y=None, sample_weight=None):
        """ Equivalent to fit(X).transform(X)

        Parameters
        ----------
        X : Triangle-like
            Set of LDFs based on the model.
        y : Ignored
        sample_weight : Ignored

        Returns
        -------
            X_new : New triangle with transformed attributes.
        """
        self.fit(X)
        return self.transform(X)
