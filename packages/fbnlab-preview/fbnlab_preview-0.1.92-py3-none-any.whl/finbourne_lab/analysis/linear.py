from __future__ import annotations

from typing import Optional
from typing import Union, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pandas import DataFrame
from statsmodels.regression.quantile_regression import QuantReg

_cms_scheme = {
    'scatter_plot': {'color': 'black', 'alpha': 0.5},
    'median_line': {'color': 'black', 'ls': '--', 'lw': 2},
    'outer_band': {'color': 'lime', 'alpha': 1.0},
    'inner_band': {'color': 'yellow', 'alpha': 1.0},
}


def _make_monochrome_scheme(c):
    return {
        'scatter_plot': {'color': c, 'alpha': 0.667},
        'median_line': {'color': c, 'ls': '--', 'lw': 2},
        'outer_band': {'color': c, 'alpha': 1 / 6},
        'inner_band': {'color': c, 'alpha': 1 / 3},
    }


class LinearModel:
    """This class encapsulates the analysis of how an attribute of an experiment scales with a single input value.

    It consists of a set of quantile regressions that put bounds on the scaling behaviour alongside helper methods
    for plotting this relationship, getting its parameters and predicting its values.

    """

    quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]

    def __init__(self, data: DataFrame, x: str, y: str, name: str, c_err_warn=0.15, m_err_warn=0.05):
        """The constructor method of the scaling model.

        Args:
            data (DataFrame): dataframe from an experimental run.
            x (str): the independent variable column name in the dataframe.
            y (str): the dependent variable column name in the dataframe.
            name (str): the name of the model,
            c_err_warn: value of intercept (c) fractional error to warn user and suggest getting more data. Default = 0.15.
            m_err_warn: value of gradient (m) fractional error to warn user and suggest getting more data. Default = 0.05.

        """

        if len(data) == 0:
            raise ValueError('The model input dataframe was empty.')

        if 'errored' in data.columns:
            data = data[(~data.errored)]
        if 'force_stopped' in data.columns:
            data = data[(~data.force_stopped)]

        data = data[~data[y].isna()]
        data = data[~data[x].isna()]

        self.data = data.reset_index(drop=True).copy()

        if self.data.shape[0] == 0:
            raise ValueError(f"There was no valid data to use ({name})")

        self.x = x
        self.y = y
        self.name = name

        x_vals = self.data[self.x].astype(float)
        y_vals = self.data[self.y].astype(float)
        model = QuantReg(y_vals, sm.add_constant(x_vals))

        self.fits = {q: model.fit(q) for q in self.quantiles}

        fr = self.fit_results()
        count = 0
        for q, row in fr.iterrows():
            me = row.m_frac_err.round(3)
            ce = row.c_frac_err.round(3)
            if ce > c_err_warn:
                print(f'⚠️ {name} quantile {q} line has a frac error on c over threshold ({ce} > {c_err_warn})')
                count += 1
            if me > m_err_warn:
                print(f'⚠️ {name} quantile {q} line has a frac error on m over threshold ({me} > {m_err_warn})')
                count += 1
        if count > 0:
            print('Consider gathering more data or removing outliers (.remove_outliers())')

    def predict(self, x: Union[float, List[float], np.array]) -> DataFrame:
        """Predict the 5th, 25th, 50th, 75th and 95th percentiles for given values of the experiment input value.

        Args:
            x (Union[float, List[float], np.array]): a single input value, or array of values, to predict for.

        Returns:
            DataFrame: a dataframe with a row for each value of x and a column for each percentile.
        """
        output = {}

        for q, m in self.fits.items():
            if isinstance(x, (float, int)):
                _x = np.asarray([x, 0]).reshape(-1, 1)
                _x = sm.add_constant(_x)
                output[q] = m.predict(_x)[0]
            elif len(x) == 1:
                _x = np.asarray([x[0], 0]).reshape(-1, 1)
                _x = sm.add_constant(_x)
                output[q] = m.predict(_x)[0]
            else:
                _x = np.asarray(x)
                _x = sm.add_constant(_x)
                output[q] = m.predict(_x)

        if isinstance(x, (float, int)) or len(x) == 1:
            ex_df = DataFrame([output])
        else:
            ex_df = DataFrame(output)

        ex_df['x'] = x
        ex_df = ex_df.set_index('x')
        return ex_df

    def fit_results(self) -> DataFrame:
        """Returns a summary dataframe containing the parameters, p values and std errors for each quantile regression
        line in the model.

        Returns:
            DataFrame: data frame with the fit results.
        """
        rows = []
        for q, m in self.fits.items():
            m.conf_int()
            rows.append({
                'quantile': q,
                'c': m.params[0],
                'm': m.params[1],
                'c_stderr': m.bse[0],
                'm_stderr': m.bse[1],
            })

        fr_df = DataFrame(rows).set_index('quantile')
        fr_df['c_frac_err'] = fr_df['c_stderr'] / abs(fr_df['c'])
        fr_df['m_frac_err'] = fr_df['m_stderr'] / abs(fr_df['m'])
        return fr_df

    def outliers(self) -> DataFrame:
        """Get lines in the input data that might be outliers according to the fit model.

        Data points are flagged as outliers if they are above the upper quartile + 1.5 * the interquartile range (IQR)
        or are below the lower quartile - 1.5 * IQR.

        Returns:
            DataFrame: dataframe of rows in the input data that may be outliers.
        """
        odf = self.predict(self.data[self.x].values).reset_index()
        odf['IQR'] = odf[0.75] - odf[0.25]
        odf['y'] = self.data[self.y].values
        lower_lim = odf[0.25] - 1.5 * odf['IQR']
        upper_lim = odf[0.75] + 1.5 * odf['IQR']
        odf = odf[~odf.y.between(lower_lim, upper_lim)]
        return self.data[self.data.index.isin(odf.index)]

    def remove_outliers(self) -> LinearModel:
        """Fit a model, remove outliers from the input data and then fit a new model.

        Returns:
            LinearModel: a new scaling model fit to data with outliers removed
        """
        outliers = self.outliers()
        data = pd.merge(self.data, outliers, indicator=True, how='outer')
        data = data.query('_merge=="left_only"').drop('_merge', axis=1)
        return LinearModel(data, self.x, self.y, self.name)

    def add_plot(self, ax, color_scheme: Optional[str] = 'cms', show_datapoints: Optional[bool] = True):

        """Add a plot of this scaling model's quantile bands, its median line and the data points that the model was
        fit with to a matplotlib axes object.

        Args:
            ax: the matplotlib axes to draw the plot on.
            color_scheme (str): the color scheme to use. This can be either 'cms' (for a CERN CMS-style brazil band) or
            any valid matplotlib named color.
            show_datapoints (bool): show the observed datapoints. Set to false if a comparison plot's getting too busy.

        """
        if color_scheme == 'cms':
            scheme = _cms_scheme
        else:
            scheme = _make_monochrome_scheme(color_scheme)

        if show_datapoints:
            ax.scatter(
                self.data[self.x],
                self.data[self.y],
                s=10, zorder=99,
                label=f'Observation ({self.name})',
                **scheme['scatter_plot']
            )

        x_min = self.data[self.x].min()
        x_max = self.data[self.x].max()

        x = np.linspace(x_min, x_max, 3)
        pred = self.predict(x)

        ax.plot(x, pred[0.5], label=f'Median ({self.name})', **scheme['median_line'])
        ax.fill_between(x, pred[0.25], pred[0.75], label=f'p25-p75 Range ({self.name})', **scheme['inner_band'])
        ax.fill_between(x, pred[0.75], pred[0.95], label=f'p5-p95 Range ({self.name})', **scheme['outer_band'])
        ax.fill_between(x, pred[0.05], pred[0.25], **scheme['outer_band'])

    def show(self, save_to=None):
        """Generate and show a single plot of this relationship

        """
        f, ax = plt.subplots(figsize=(12, 7))
        self.add_plot(ax)
        plt.xlabel(self.x)
        plt.ylabel(self.y)
        plt.legend()
        plt.grid(True, ls=':', zorder=-99)
        if save_to:
            plt.savefig(save_to)
        plt.show()

    def __sub__(self, other: LinearModel) -> LinearModel:

        x = self.data[self.x].values
        y = self.data[self.y].values
        y_pred = other.predict(x)[0.5].values
        delta = y - y_pred

        df = self.data
        label = f'{self.y}_sub_{other.y}'
        df[label] = delta

        return LinearModel(df, self.x, label, f'{self.name} - {other.name}')

    def __add__(self, other: LinearModel) -> LinearModel:

        x = self.data[self.x].values
        y = self.data[self.y].values
        total = y + other.predict(x)[0.5].values

        df = self.data
        label = f'{self.y}_total_{other.y}'
        df[label] = total

        return LinearModel(df, self.x, label, f'{self.name} + {other.name}')

    def __truediv__(self, other: LinearModel) -> LinearModel:

        x = self.data[self.x].values
        y = self.data[self.y].values
        ratio = y / other.predict(x)[0.5].values

        df = self.data
        label = f'{self.y}_div_{other.y}'
        df[label] = ratio

        return LinearModel(df, self.x, label, f'{self.name} / {other.name}')

    def __mul__(self, other: LinearModel) -> LinearModel:

        x = self.data[self.x].values
        y = self.data[self.y].values
        y_pred = other.predict(x)[0.5].values
        prod = y * y_pred

        df = self.data
        label = f'{self.y}_prod_{other.y}'
        df[label] = prod

        return LinearModel(df, self.x, label, f'{self.name} * {other.name}')

    def merge(self, other, name=None):
        """Merge the underlying data of two linear scaling models together and re-fit

        Args:
            other (LinearModel): the other model
            name (str): name to give the result of the merge

        Returns:
            LinearModel: the new scaling model from the merged data
        """

        if self.x != other.x or self.y != other.y:
            raise ValueError(
                f'x and y must match when merging models but were different. '
                f'x: {self.x} vs {other.x}, y: {self.y} vs {other.y}'
            )

        data_l = self.data
        data_r = other.data
        data = pd.concat([data_l, data_r])
        return LinearModel(data, self.x, self.y, f"{self.x}_{self.y}" if name is None else name)

    def to_csv(self, filepath):
        """Export the constituent dataset this model is derived from to a CSV

        Args:
            filepath (str): the path to write the csv at.

        """
        self.data.to_csv(filepath, index=False)

    def ab_test(self, b_model):
        """Construct an A/B test between this linear model and another.

        Args:
            b_model (LinearModel): the b-sample linear model

        Returns:
            ScalingModelABTest: object encapsulating the A/B test result.
        """
        from .ab_test import ScalingModelABTest
        return ScalingModelABTest(self, b_model)
