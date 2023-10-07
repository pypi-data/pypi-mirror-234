"""
Calculates the fair value of a stock based on different methods.
No warranty for correctness of the results.
"""
from datetime import datetime
from math import sqrt
from typing import List, Tuple


class FairValueCalculatorBase:

    @staticmethod
    def calc_fair_value_base(expected_per_share_value: float, expected_multiple: float):
        """
        Calculates the fair value based on the given expected_per_share_value (e.g. expected earnings per share) and the
        expected_multiple (e.g. price earnings ratio)
        :param expected_per_share_value: The expected value on share base like future EPS or Sales/Share
        :param expected_multiple: The expected multiple like PE ratio or PS ratio
        :return: the fair value of the stock based on the given inputs
        """
        return expected_per_share_value * expected_multiple

    @staticmethod
    def calc_fair_value_with_growth(current_per_share_value: float, expected_multiple: float,
                                    growth_rate_per_year: float, number_of_years: int = 5) -> List[Tuple[int, float]]:
        """
        Calculate the fair value based on the current per share value, the expected multiple and the
        growth rate per year for the future
        :param current_per_share_value: The current value on share base like actual EPS or Sales/Share
        :param expected_multiple: The expected multiple like PE ratio or PS ratio
        :param growth_rate_per_year: The rate of growth per year in percent
        :param number_of_years: The number of years to calculate the fair value in the future, with the
                                expected growth rate
        :return: The list of fair value of tuples of the form (<year_in_the_future>, <fair_value_for_year>)
        """
        current_year = datetime.now().year
        growth_to_use = growth_rate_per_year / 100.0 + 1
        return [(current_year + i, expected_multiple * current_per_share_value * growth_to_use ** i) for i in
                range(1, number_of_years + 1)]

    @staticmethod
    def calc_fair_value_graham_dcf(earnings_per_share: float, growth_rate: float, ten_years_gov_bond_rate: float):
        """
        Calculates the fair value based on the benjamin graham formula.
        Formula: (earnings_per_share * (8.5 + 2 * growth_rate) * 4.4) / ten_years_gov_bond_rate
        :param earnings_per_share: The current earnings per share of the company
        :param growth_rate: The expected growth rate for the growth per year of the earnings
        :param ten_years_gov_bond_rate: The current yield of the ten years government bond
        :return: The fair value of the stock based on the simple graham dcf formula
        """
        return (earnings_per_share * (8.5 + 2 * growth_rate) * 4.4) / ten_years_gov_bond_rate

    @staticmethod
    def calc_fair_value_graham_number(earnings_per_share: float, book_value_per_share: float):
        """
        Calculates the fair value based on the benjamin graham number.
        Formula: sqrt((22.5 (fair PE-Ratio) * earnings_per_share * book_value_per_share)
        :param earnings_per_share: The current earnings per share of the company
        :param book_value_per_share: The current book value per share of the company
        :return: The fair value based on the graham number
        """
        return sqrt(22.5 * earnings_per_share * book_value_per_share)
