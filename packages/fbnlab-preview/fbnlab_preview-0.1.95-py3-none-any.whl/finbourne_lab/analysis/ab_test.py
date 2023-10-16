from statsmodels.regression.quantile_regression import QuantReg
import statsmodels.api as sm
from .linear import LinearModel
import pandas as pd
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest
from scipy.special import ndtr
from math import floor
from .distribution import Distribution


class DistributionABTest:
    """Class that encapsulates logic for performing a Kolmogorov-Smirnov test, evaluating effect sizes, and plotting results.

    References:
        https://en.wikipedia.org/wiki/Kolmogorov–Smirnov_test

    """

    def __init__(self, a_dist: Distribution, b_dist: Distribution):
        """Constructor for the distribution A/B test

        Args:
            a_dist (Distribution): distribution object of the A sample.
            b_dist (Distribution): distribution object of the B sample.

        """
        if a_dist.x != b_dist.x:
            raise ValueError(f'The x columns do not match between the histograms (A: {a_dist.x}, B: {b_dist.x}')
        if a_dist.name == b_dist.name:
            raise ValueError('A model and B model must have different names.')

        self.a_dist = a_dist
        self.b_dist = b_dist

    def evaluate_h0(self, n_sigma: Optional[int] = 5):
        """Evaluate the null hypothesis for this A/B test for a given rejection threshold. This class uses the scipy
        implementation of a Kolmogorov-Smirnov test.

            https://en.wikipedia.org/wiki/Kolmogorov–Smirnov_test

        Notes:
            The null hypothesis (H_0) is the hypothesis that there is no significant difference between the A and B
            samples. This is modelled by the 'null distribution' the probability distribution of the statistic when
            there is no effect. If the observed difference between A and B is sufficiently rare (low probability according
            to the null distribution) we reject the null hypothesis and consider the difference to be significant.

            The canonical example of this is the 'Lady tasting tea' experiment by Ronald Fisher
                https://en.wikipedia.org/wiki/Lady_tasting_tea

            A p value is not a measure of the likelihood that the effect is real - we can't know this for sure. It is a
            measure of how unusual the observed effect is assuming our null hypothesis holds.

        Args:
            n_sigma (Optional[int]): the rejection threshold given as n-many standard deviations.

        Returns:
            DataFrame: a DataFrame containing information on the hypothesis test: the statistic, the p value,
            the probability threshold that we reject H_0 at, and whether H_0 is indeed rejected.

        """
        res = kstest(self.a_dist.vals, self.b_dist.vals)
        threshold = 1 - ndtr(n_sigma)
        return pd.DataFrame([{
            'KS_Statistic': res.statistic,
            'PValue': res.pvalue,
            'Threshold': threshold,
            'H0_Rejected': res.pvalue < threshold
        }])

    def effect_sizes(self):
        """Return a dataframe quantile differences (effect sizes) between A and B that include arithmetic and fractional
        differences.

        Returns:
            DataFrame: dataframe containing effect size data.

        """

        es_df = pd.concat([
            self.a_dist.quantiles_df(),
            self.b_dist.quantiles_df()
        ]).reset_index(drop=True).T

        es_df.columns = ['A', 'B']
        es_df['Diff'] = es_df.B - es_df.A
        es_df['FracDiff'] = (es_df.B - es_df.A) / es_df.A.abs()
        return es_df

    def plot(self, n_sigma: Optional[int] = 5, save_to: Optional[str] = None, bins: Optional[int] = None):
        """

        Args:
            n_sigma (int): number of sigmas deviation (z score) to consider a significant deviation.
            save_to (Optional[str]): filepath to save the plot to. If not given then nothing will be saved.
            bins (Optional[int]): number of bins to use in the histogram subplot.

        Returns:
            Tuple: the figure, axes, and whether the null hypothesis was rejected

        """

        if bins is None:
            bins = min(100, round(((self.a_dist.n + self.b_dist.n) * 0.5) ** 0.5))

        quantiles = self.a_dist.quantiles_default

        rng = [
            min(self.a_dist.min, self.b_dist.min),
            max(self.a_dist.max, self.b_dist.max),
        ]

        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Histograms
        self.a_dist.add_hist(ax1, bins=bins, color='grey', rng=rng)
        self.b_dist.add_hist(ax1, bins=bins, color='red', rng=rng)
        ax1.set_ylabel('Probability Density')
        ax1.set_xlabel(f'$x$ ({self.a_dist.x})')
        ax1.legend()
        ax1.set_xlim(*rng)
        ax1.grid(True, ls=':')
        ax1.set_title('Probability Distributions')

        # Empirical CDFs
        self.a_dist.add_ecdf(ax2, rng=rng, color='grey')
        self.b_dist.add_ecdf(ax2, rng=rng, color='red')
        ax2.set_ylabel('ECDF')
        ax2.set_xlim(*rng)
        ax2.set_xlabel(f'$x$ ({self.a_dist.x})')
        ax2.legend(loc=2)
        ax2.grid(True, ls=':')
        for q in quantiles:
            ax2.axhline(q, color='blue', alpha=0.75, ls=':')
            ax3.axhline(q, color='blue', alpha=0.75, ls=':')
        ax2.set_title('Empirical Cumulative Distribution Functions')

        # Quantile shift plot
        e_df = self.effect_sizes()
        ax3.set_title('Effect Sizes\n(Quantile Shifts)')
        ax3.barh(e_df.index, e_df.Diff, color='blue', alpha=0.25, height=0.1)
        ax3.set_yticks(e_df.index)
        ax3.set_yticklabels(e_df.index)
        ax3.set_ylabel('Quantile')
        ax3.set_xlabel('$Q(q; x_B) - Q(q; x_A)$')
        ax3.axvline(0, color='black')
        ax3.grid(True, ls=':')

        h0 = self.evaluate_h0(n_sigma).iloc[0]

        if h0.H0_Rejected:
            h0_str = '$H_0$ is rejected'
        else:
            h0_str = '$H_0$ is not rejected'

        def to_latex(x, dp=3):
            if x == 0:
                return '0'
            order = floor(np.log10(x))
            val = x / (10 ** order)
            return f'{round(val, dp)} \\times 10^{{{order}}}'

        caption = f'''Two-Sided Kolmogorov-Smirnov Test Results

        KS test statistic: $D = {to_latex(h0.KS_Statistic)}$
        p value: $p = {to_latex(h0.PValue)}$
        Rejection threshold: $p_{{th}} = {to_latex(h0.Threshold)}$

        The null hypothesis {h0_str} at ${n_sigma}\sigma$
        '''

        plt.figtext(0.5, -0.0, caption, wrap=True, verticalalignment='top', horizontalalignment='center', fontsize=12)

        plt.tight_layout()

        if save_to is not None:
            plt.savefig(save_to, bbox_inches='tight')

        return f, (ax2, ax1), h0.H0_Rejected


class ScalingModelABTest:
    """Class that encapsulates an A/B test between two linear scaling models.

    The A/B analysis consists of a linear quantile regression to the combined dataset of the two models where the model contains
    a condition term and an interaction term (y ~ x + const + condition + x:condition). A difference between the
    coefficients of the condition or interaction term is considered significant (null hypothesis that the models are the
    same is rejected) when their p values are below a set threshold. This is 4 sigma by default.

    This procedure is carried out for each quantile line.

    """

    def __init__(self, a_model: LinearModel, b_model: LinearModel):
        """Constructor for the ScalingModelABTest class.

        Args:
            a_model (LinearModel): scaling model of the A sample.
            b_model (LinearModel): scaling model of the B sample.

        """

        if a_model.x != b_model.x:
            raise ValueError(f'The x columns do not match between the models (A: {a_model.x}, B: {b_model.x}')
        # commented out until we come up with a better check
        # if a_model.y != b_model.y:
        #     raise ValueError(f'The y columns do not match between the models (A: {a_model.y}, B: {b_model.y}')
        if a_model.name == b_model.name:
            raise ValueError('A model and B model must have different names.')

        self.a_model = a_model
        self.b_model = b_model

        self.x = a_model.x
        self.y = 'ab_y_value'

        a_df = a_model.data
        a_df['delta_c'] = 0
        a_df[self.y] = a_df[a_model.y]

        b_df = b_model.data
        b_df['delta_c'] = 1
        b_df[self.y] = b_df[b_model.y]

        self.df = pd.concat([a_df, b_df])
        self.df['delta_m'] = self.df[self.x] * self.df['delta_c']

        model = QuantReg(
            self.df[self.y],
            sm.add_constant(self.df[[self.x, 'delta_c', 'delta_m']])
        )
        self.quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        self.fits = {q: model.fit(q) for q in self.quantiles}

    def fit_result(self):
        """Returns a summary dataframe containing the parameters, p values and std errors for each quantile regression
        line in the combined model.

        Returns:
            DataFrame: data frame with the fit results.

        """

        # model params by quantile
        p_df = pd.concat(pd.DataFrame(self.fits[q].params).T for q in self.quantiles)
        p_df['quantile'] = self.quantiles
        p_df = p_df.set_index('quantile')

        # standard errors on model params
        e_df = pd.concat(pd.DataFrame(self.fits[q].bse).T for q in self.quantiles)
        e_df['quantile'] = self.quantiles
        e_df = e_df.set_index('quantile')

        return pd.merge(p_df, e_df, on='quantile', suffixes=('', '_stderr'))

    def evaluate_h0(self, n_sigma: Optional[int] = 5):
        """Evaluate the null hypothesis for this A/B test for a given rejection threshold.

        The A/B analysis consists of a linear quantile regression to the combined dataset of the two models where the model contains
        a condition term and an interaction term (y ~ x + const + condition + x:condition). A difference between the
        coefficients of the condition or interaction term is considered significant (null hypothesis that the models are the
        same is rejected) when their p values are below a set threshold. This is 4 sigma by default.

        Notes:
            The null hypothesis (H_0) is the hypothesis that there is no significant difference between the A and B
            samples. This is modelled by the 'null distribution' the probability distribution of the statistic when
            there is no effect. If the observed difference between A and B is sufficiently rare (low probability according
            to the null distribution) we reject the null hypothesis and consider the difference to be significant.

            The canonical example of this is the 'Lady tasting tea' experiment by Ronald Fisher
                https://en.wikipedia.org/wiki/Lady_tasting_tea

            A p value is not a measure of the likelihood that the effect is real - we can't know this for sure. It is a
            measure of how unusual the observed effect is assuming our null hypothesis holds.

        Args:
            n_sigma (Optional[int]): the rejection threshold given as n-many standard deviations.

        Returns:
            DataFrame: a DataFrame containing information on the hypothesis test: the statistic, the p value,
            the probability threshold that we reject H_0 at, and whether H_0 is indeed rejected.

        """

        threshold = 1 - ndtr(n_sigma)

        pv_df = pd.concat(pd.DataFrame(self.fits[q].pvalues).T for q in self.quantiles)
        pv_df['quantile'] = self.quantiles
        pv_df['threshold'] = threshold
        pv_df['reject_h0_c'] = (pv_df['delta_c'] < threshold)
        pv_df['reject_h0_m'] = (pv_df['delta_m'] < threshold)
        pv_df['reject_h0'] = pv_df.reject_h0_c | pv_df.reject_h0_m

        return pv_df.set_index('quantile')[['delta_c', 'delta_m', 'reject_h0_c', 'reject_h0_m', 'reject_h0', 'threshold']]

    def effect_sizes(self):
        """Return a dataframe of m and c deltas (effect sizes) between A and B, deltas expressed as a fraction of m and
        c and the standard errors of the deltas as a fraction of m and c.

        Returns:
            DataFrame: dataframe containing effect size data.

        """

        fr_df = self.fit_result()
        es_df = fr_df[['delta_c', 'delta_m']].copy()
        es_df['frac_diff_c'] = fr_df['delta_c'] / fr_df['const']
        es_df['frac_diff_m'] = fr_df['delta_m'] / fr_df[self.x]
        es_df['frac_diff_c_stderr'] = abs(fr_df['delta_c_stderr'] / fr_df['const'])
        es_df['frac_diff_m_stderr'] = abs(fr_df['delta_m_stderr'] / fr_df[self.x])
        return es_df

    def plot(self, n_sigma=5, save_to=None):
        """Create a summary plot that shows deltas for m and c with the statistically significant ones highlighted
        in red.

        Args:
            n_sigma (int): number of sigmas deviation (z score) to consider a significant deviation.
            save_to (Optional[str]): filepath to save the plot to. If not given then nothing will be saved.

        Returns:
            Tuple[Figure, AxesSubplot]: matplotlib figure and subplot objects of the plot.

        """

        es_df = self.effect_sizes()
        h0_df = self.evaluate_h0(n_sigma)

        f, axd = plt.subplot_mosaic([['top', 'top'], ['left', 'right']], figsize=(14, 10))

        ax1 = axd['right']
        ax2 = axd['left']
        ax3 = axd['top']

        self.a_model.add_plot(ax3, color_scheme='grey')
        self.b_model.add_plot(ax3, color_scheme='blue')
        ax3.legend()
        ax3.set_title('Model Comparison', fontsize=13)
        ax3.set_xlabel(f'$x$ ({self.a_model.x})', fontsize=13)
        ax3.set_ylabel(f'$y$ ({self.a_model.y})', fontsize=13)
        ax3.grid(True, ls=':')

        y = np.arange(0, es_df.shape[0]) * 2

        ax1.axvline(0, lw=2, ls='-', color='black', label='No Effect')
        ax2.axvline(0, lw=2, ls='-', color='black', label='No Effect')

        ms = 6
        errbar_factor = 2

        # gradients
        ax1.errorbar(
            100 * es_df.frac_diff_m, y + 1, xerr=100 * es_df.frac_diff_m_stderr * errbar_factor,
            ls='none', marker='o', color='black', markerfacecolor='white', markersize=ms,
            capsize=5,
            label=f'$\Delta{{m}} \pm{errbar_factor}\sigma$'
        )
        ax1.set_title('Gradient Effect ($\Delta{m}$)', fontsize=13)

        # intercepts
        ax2.errorbar(
            es_df.frac_diff_c * 100, y + 1, xerr=100 * es_df.frac_diff_c_stderr * errbar_factor,
            ls='none', marker='o', color='black', markerfacecolor='white', markersize=ms,
            capsize=5,
            label=f'$\Delta{{c}} \pm{errbar_factor}\sigma$'
        )
        ax2.set_title('Intercept Effect ($\Delta{c}$)', fontsize=13)

        red = {'color': 'red', 'alpha': 0.3}
        grey = {'color': 'grey', 'alpha': 0.15}

        for i in range(es_df.shape[0]):
            m_color = red if h0_df.reject_h0_m.iloc[i] else grey
            c_color = red if h0_df.reject_h0_c.iloc[i] else grey

            ax1.axhspan(i * 2 + 0.5, i * 2 + 1.5, **m_color)
            ax2.axhspan(i * 2 + 0.5, i * 2 + 1.5, **c_color)

        ax1.axhspan(-3, -2, label='Significant', **red)
        ax1.axhspan(-3, -2, label='Not Significant', **grey)
        ax2.axhspan(-3, -2, label='Significant', **red)
        ax2.axhspan(-3, -2, label='Not Significant', **grey)

        ax1.set_xlabel('Effect Size (%)', fontsize=13)
        ax2.set_xlabel('Effect Size (%)', fontsize=13)
        ax2.set_ylabel('Quantile', fontsize=13)
        ax1.set_ylim(0, es_df.shape[0] * 2)
        ax2.set_ylim(0, es_df.shape[0] * 2)

        ax1.grid(True, ls=':', color='black')
        ax2.grid(True, ls=':', color='black')
        ax1.set_yticks(y + 1)
        ax1.set_yticklabels(es_df.index)
        ax2.set_yticks(y + 1)
        ax2.set_yticklabels(es_df.index)

        ax2.legend()
        ax1.legend()

        caption = f'''
        The combined linear model is:
            $y = c + mx + \Delta{{c}}\delta + \Delta{{m}}x\delta$
        
        where:
            $x$ is {self.x}, $y$ is {self.y}, $m$ is the gradient, $c$ is the 
            intercept, $\delta$ is the A/B condition variable which is 0 when an 
            entry is from sample A and 1 from sample B, $\Delta{{m}}$ is the gradient 
            difference between the A/B samples, and $\Delta{{c}}$ is the intercept 
            difference between the A/B samples. 
        '''
        plt.figtext(0.3, -0.0, caption, wrap=True, verticalalignment='top', horizontalalignment='left', fontsize=12)

        plt.tight_layout()
        f.subplots_adjust(hspace=0.2)

        if save_to is not None:
            plt.savefig(save_to, bbox_inches='tight')

        return f, (ax1, ax2, ax3)
