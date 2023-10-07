"""Class maintaining the plotting functionality for SECUnit entries."""
from enum import Enum
from typing import List, Tuple

import matplotlib.pyplot as plt
import seaborn as sns

from ..data_representation.SECUnits import SECUnits


class NumberFormat(Enum):
    """Enum for defining the number format."""
    PLAIN = 0
    THOUSANDS = 1
    MILLIONS = 2
    BILLIONS = 3
    TRILLIONS = 4


class SECUnitPlotter:
    _palette = None

    def __init__(self, color_palette=None):
        sns.set_theme()

        if color_palette is not None:
            self._palette = sns.color_palette("coolwarm", as_cmap=True)
        else:
            self._palette = color_palette

    def _apply_number_format(self, list_of_values: List[float], number_format: NumberFormat) -> Tuple[List[float], str]:
        return [round(val / 10 ** (3 * number_format.value), 3) for val in list_of_values], number_format.name

    def _determine_auto_format(self, list_of_values: List[float]) -> NumberFormat:
        smallest_val = min(list_of_values)

        if (smallest_val / 10 ** (3 * NumberFormat.TRILLIONS.value)) > 1:
            return NumberFormat.TRILLIONS
        elif (smallest_val / 10 ** (3 * NumberFormat.BILLIONS.value)) > 1:
            return NumberFormat.BILLIONS
        elif (smallest_val / 10 ** (3 * NumberFormat.MILLIONS.value)) > 1:
            return NumberFormat.MILLIONS
        elif (smallest_val / 10 ** (3 * NumberFormat.THOUSANDS.value)) > 1:
            return NumberFormat.THOUSANDS
        elif (smallest_val / 10 ** (3 * NumberFormat.PLAIN.value)) > 1:
            return NumberFormat.PLAIN

    def plot_sec_units_base(self, sec_units: List[SECUnits], kind: str = "bar",
                            number_format: NumberFormat = None,
                            auto_number_format: bool = True, title: str = None):
        """
        Base functionality for plotting a list of SECUnit entries
        :param title: The title of the plot
        :param auto_number_format: In case no number format is passed and auto number format should be used,
            the best format suitable format is chosen for displaying
        :param number_format: The number format to use for displaying the y-values
        :param kind: The kind of plot either bar or line chart
        :param sec_units: The list of SECUnits to plot
        """
        sec_units_ordered = sorted(sec_units, key=lambda x: x.end)

        if len(sec_units_ordered) == 0:
            raise AttributeError("Empty List passed for plotting the SECUnits!")

        x_values = [unit.end.strftime("%Y-%m-%d") for unit in sec_units_ordered]
        y_values = [unit.val for unit in sec_units_ordered]

        if number_format is None and auto_number_format:
            number_format = self._determine_auto_format(y_values)

        if number_format is not None and number_format.value != 0:
            y_values, format_label = self._apply_number_format(y_values, number_format)
            plt.ylabel(f"({sec_units_ordered[-1].unit}) in {format_label}")

        if kind == "bar":
            ax = sns.barplot(x=x_values, y=y_values, palette=self._palette, color='b')
        elif kind == "line":
            ax = sns.lineplot(x=x_values, y=y_values, palette=self._palette)
        else:
            raise AttributeError("Passed unsupported type for kind of plot. Parameter 'kind' can only take values "
                                 "'line' or 'bar'")

        plt.xticks(rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        if title is not None:
            plt.title(title)
        plt.show()
