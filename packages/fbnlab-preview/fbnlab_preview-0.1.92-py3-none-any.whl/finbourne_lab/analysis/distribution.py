from typing import Union, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF


class Distribution:
    """Class that encapsulates data and operations on a univariate sample.

    """

    quantiles_default = [0.05, 0.25, 0.5, 0.75, 0.95]

    def __init__(self, data: pd.DataFrame, x: str, name: str):
        """Constructor for the distribution class.

        Args:
            data (DataFrame): data to use.
            x (str): the name of the column to use.
            name (str): the name to label the distribution with.

        """

        if len(data) == 0:
            raise ValueError('The model input dataframe was empty.')

        if 'errored' in data.columns:
            data = data[(~data.errored)]
        if 'force_stopped' in data.columns:
            data = data[(~data.force_stopped)]

        self.data = data.copy()

        if self.data.shape[0] == 0:
            raise ValueError(
                f"There was no non-errored data to use from the experiment {data.iloc[0].ExperimentName}!"
            )

        self.n = self.data.shape[0]
        self.x = x
        self.name = name
        self.vals = self.data[x]

        self.min = min(self.vals)
        self.max = max(self.vals)

        self.ecdf = ECDF(self.vals)

    def quantiles_df(self):
        """A dataframe containing the quantiles 0.05, 0.25, 0.5, 0.75 and 0.95 indexed by name.

        The dataframes produced by this method are ready to be concatenated together with pd.concat.

        Returns:
            DataFrame: the dataframe containing the quantiles.

        """
        df = pd.DataFrame(self.data[self.x].quantile(self.quantiles_default)).T
        df['name'] = self.name
        df = df.reset_index(drop=True)
        return df.set_index('name')

    def quantile(self, q: Union[float, List[float]]):
        """Compute a quantile or set of quantiles from the distribution.

        Args:
            q (Union[float, List[float]]): quantile value or list of quantile values to calculate

        Returns:
            np.array: numpy array of values

        """
        return np.quantile(self.vals, q)

    def outliers(self):
        """Derive a dataframe of outliers where outliers are identified as outside the range

            (lower quartile - 1.5 * IQR, upper quartile + 1.5 * IQR)

        where IQR is the inter-quartile range

        Returns:
            DataFrame: pandas dataframe containing the data rows identified as outliers.

        """
        iqr = self.quantile(0.75) - self.quantile(0.25)
        lower = self.quantile(0.25) - iqr * 1.5
        upper = self.quantile(0.75) + iqr * 1.5
        return self.data[~self.data[self.x].between(lower, upper)]

    def remove_outliers(self):
        """Create a new distribution object with the outliers removed.

        Outliers are identified as outside the range

            (lower quartile - 1.5 * IQR, upper quartile + 1.5 * IQR)

        where IQR is the inter-quartile range

        Returns:
            Distribution: the distribution with outliers removed.

        """
        iqr = self.quantile(0.75) - self.quantile(0.25)
        lower = self.quantile(0.25) - iqr * 1.5
        upper = self.quantile(0.75) + iqr * 1.5
        df = self.data[self.data[self.x].between(lower, upper)]
        return Distribution(df, self.x, self.name)

    def add_hist(self, ax, bins=None, density=True, color='red', alpha=0.4, label=None, rng=None):
        """Add a histogram of these data to the given matplotlib axes.

        Args:
            ax: the axes to draw the histogram on
            bins (Optional[int]): number of bins to use in the histogram. Will default to sqrt of number of datapoints
            or 100 - whichever is smaller.
            density (Optional[bool]): whether the histogram is normalised.
            color (Optional[str]): the color to use in the histogram (defaults to red)
            alpha (Optional[float]): the alpha value to use when drawing the histogram (defaults to 0.4)
            label (Optional[str]): the label to use to label the histogram in the plot (name in legend). If not
            specified it'll be the name of this distribution.
            rng (Optional[Tuple]): x-range of the histogram. If not specified it'll be the min/max of this distribution.

        """

        if bins is None:
            bins = min(100, int(self.n**0.5))

        if label is None:
            label = self.name

        ax.hist(self.vals, bins, density=density, color=color, alpha=alpha, label=label, range=rng)

    def add_ecdf(self, ax, color='red', alpha=0.5, label=None, lw=2, rng=None):
        """

        Args:
            ax: the axes to draw the cumulative distribution function on.
            color (Optional[str]): the color to use in the CDF line (defaults to red)
            alpha (Optional[float]): the alpha value to use when drawing CDF line (defaults to 0.5)
            label (Optional[str]): the label to use to label the CDF line in the plot (name in legend). If not
            specified it'll be the name of this distribution.
            lw (Optional[int]): the width of the CDF line (defaults to 2).
            rng (Optional[Tuple]): x-range of the CDF line. If not specified it'll be the min/max of this distribution.

        """

        if rng is None:
            rng = [self.min, self.max]
        if label is None:
            label = self.name

        x = np.linspace(*rng, 100)

        ax.plot(x, self.ecdf(x), color=color, alpha=alpha, lw=lw, label=label)

    def show(self, bins=None):
        """Plot a histogram of this distribution.

        Args:
            bins (Optional[int]): number of bins in the histogram

        """

        f, ax = plt.subplots(1, 1, figsize=(6, 5))
        self.add_hist(ax, bins=bins)
        ax.grid(True, ls=':')
        ax.set_xlabel(self.x)
        ax.set_ylabel('Probability Density')
        ax.legend()
        plt.show()

    def ab_test(self, other):
        """Build an A/B test object for this distribution (A) vs another (B).

        Args:
            other (Distribution): the other distribution (B)

        Returns:
            DistributionABTest: the A/B test for the two distributions.
        """
        from .ab_test import DistributionABTest
        return DistributionABTest(self, other)
