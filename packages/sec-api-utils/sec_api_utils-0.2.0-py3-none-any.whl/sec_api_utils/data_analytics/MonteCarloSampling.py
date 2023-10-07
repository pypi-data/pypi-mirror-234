"""Provides Monte Carlo sampling functions for data analytics to compare baskets of stocks."""
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class MonteCarloSampler:


    @staticmethod
    def generate_random_returns_for_single_path(mean, std, num_years):
        """
        Generates random returns based on a normal distribution for a single path.

        :param mean: float
            Mean of the normal distribution.
        :param std: float
            Standard deviation of the normal distribution.
        :param num_years: int
            Number of samples to generate.
        :return: Array of random returns.
        """
        return np.random.normal(mean, std, num_years)

    def generate_random_returns_for_multiple_paths(self, mean, std, num_years, num_paths):
        """
        Generates random returns based on a normal distribution for multiple paths.

        :param mean: float
            Mean of the normal distribution.
        :param std: float
            Standard deviation of the normal distribution.
        :param num_years: int
            Number of samples to generate.
        :param num_paths: int
            Number of paths to generate.

        :return: Array of random return paths.
        """
        return np.array([self.generate_random_returns_for_single_path(mean, std, num_years) for _ in range(num_paths)])

    @staticmethod
    def calc_yearly_mean_and_df(returns: Union[np.array, pd.Series]):
        """
        Calculates mean and standard deviation of a series of returns from daily or more frequent data.
        Due to the central limit theorem, the mean and standard deviation of the yearly aggregated data of
        daily or more frequent data approach a normal distribution.

        Since the sum of daily returns is equal to the yearly return.

        :param returns: Array of returns.
        :return: Tuple of mean and standard deviation.
        """
        return np.mean(returns), np.std(returns)

    def plot_random_paths(self, mean, std, num_years, num_paths, benchmark_return=None, start_value=1000):
        """
        Plots random returns based on a normal distribution for multiple paths.

        :param mean: float
            Mean of the normal distribution.
        :param std: float
            Standard deviation of the normal distribution.
        :param num_years: int
            Number of samples to generate.
        :param num_paths: int
            Number of paths to generate.
        :param benchmark_return: float
            Benchmark return to beat.
        :param start_value: float
            Start value of the path.

        :return: Array of random return paths.
        """
        random_returns = self.generate_random_returns_for_multiple_paths(mean, std, num_years, num_paths)
        random_returns = 1 + random_returns
        for i in range(num_paths):
            plt.plot(start_value * np.cumprod(random_returns[i, :]), color='lightgray')

        plt.plot(start_value * np.cumprod(np.mean(random_returns, axis=0)), color='black', label='Mean of Paths')

        if benchmark_return is not None:
            plt.plot(start_value * np.cumprod([1 + benchmark_return] * num_years), color='red', label='Benchmark')
        plt.show()

    def calculate_probability_of_beating_benchmark(self, mean, std, num_years, num_paths, benchmark_return):
        """
        Calculates the probability of beating a benchmark return.

        :param mean: float
            Mean of the normal distribution.
        :param std: float
            Standard deviation of the normal distribution.
        :param num_years: int
            Number of samples to generate.
        :param num_paths: int
            Number of paths to generate.
        :param benchmark_return: float
            Benchmark return to beat.

        :return: Probability of beating benchmark return.
        """
        random_returns = self.generate_random_returns_for_multiple_paths(mean, std, num_years, num_paths)

        # Since the returns are paths, we need to aggregate them to get the total return for each path.
        annualized_returns = np.mean(random_returns, axis=1)

        return np.sum(annualized_returns > benchmark_return) / num_paths

    @staticmethod
    def calculate_terminal_value_of_path(returns: Union[np.array, pd.Series], initial_value: float = 10000):
        """
        Calculates the terminal value of a given path.

        :param returns: Array of returns.
        :param initial_value: Initial value of the path.
        :return: Terminal value of the path.
        """
        return initial_value * np.cumprod(1 + np.array(returns))[-1]

    def calculate_probability_by_terminal_value(self, mean, std, num_years, num_paths, benchmark_return):
        """
        Calculates the probability of reaching a terminal value.

        :param mean: float
            Mean of the normal distribution.
        :param std: float
            Standard deviation of the normal distribution.
        :param num_years: int
            Number of samples to generate.
        :param num_paths: int
            Number of paths to generate.
        :param benchmark_return: float
            Benchmark return value.
        :return: Probability of reaching terminal value.
        """
        random_returns = self.generate_random_returns_for_multiple_paths(mean, std, num_years, num_paths)

        start_value = 1000

        # Since the returns are paths, we need to aggregate them to get the total return for each path.
        terminal_values = np.array(
            [self.calculate_terminal_value_of_path(random_returns[i, :], start_value) for i in range(num_paths)])

        benchmark_terminal_value = self.calculate_terminal_value_of_path([benchmark_return] * num_years, start_value)

        return np.round(np.sum(terminal_values > benchmark_terminal_value) / num_paths, 2)
