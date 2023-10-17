"""Defines Lognormal Distribution."""

from scipy import stats

from simba_ml import error_handler
from simba_ml.simulation import random_generator


class LogNormalDistribution:
    """An object which samples values from a log-normal distributions.

    Attributes:
        mu: Mean ("centre") of the distributions.
        sigma: Standard deviation (spread or "width") of the distributions.
        Must be non-negative.

    Raises:
        ValueError: If sigma < 0.
        TypeError: If mu is not float or int.
        TypeError: If sigma is not float or int.
    """

    def __init__(self, mu: float, sigma: float) -> None:
        """Inits LogNormalDistribution with the provided arguments.

        Args:
            mu: Mean ("centre") of the distributions.
            sigma: Standard deviation (spread or "width") of the distributions.
                Must be non-negative.
        """
        self.mu = mu
        self.sigma = sigma

        error_handler.confirm_param_is_float_or_int(self.mu, "mu")
        error_handler.confirm_param_is_float_or_int(self.sigma, "sigma")
        error_handler.confirm_number_is_greater_or_equal_to_0(self.sigma, "sigma")

    def get_random_values(self, n: int) -> list[float]:
        """Samples an array with the given distribution.

        Args:
            n: The number of values.

        Returns:
            np.ndarray[float]
        """
        return (
            random_generator.get_rng().lognormal(self.mu, self.sigma, size=n).tolist()
        )

    def get_samples_from_hypercube(self, n: int) -> list[float]:
        """Samples n values from a hypercube.

        Args:
            n: the number of samples.

        Returns:
            Samples of the distribution, sampled from a hypercube.
        """
        p = [
            random_generator.get_rng().uniform(low=i / n, high=(i + 1) / n)
            for i in range(n)
        ]
        return stats.lognorm.ppf(p, 1, self.mu, self.sigma)
