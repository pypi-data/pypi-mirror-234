from scipy.stats import norm
from cobaya.likelihood import Likelihood


class TestLike(Likelihood):

    def initialize(self):
        self.norm = norm(loc=self.H0, scale=self.H0_std)

    def get_requirements(self):
        return {'H0': None}

    def logp(self, **params_values):
        H0_theory = self.provider.get_param("H0")
        return self.norm.logpdf(H0_theory)
