from collections import defaultdict
from pprint import pformat
from typing import List, Dict, Optional

from ..data_representation.SECUnits import SECUnits


class SECBaseMeasure:
    name: str
    label: str
    description: str
    units: List[SECUnits]
    _form_type_to_unit: Dict[str, List[SECUnits]]

    def __repr__(self):
        return pformat(self.__dict__)

    def __init__(self, name: str, label: str, description: str, units: Dict[str, List[Dict]]):
        self.name = name
        self.label = label
        self.description = description
        self.units = []
        self._form_type_to_unit = defaultdict(list)
        self._parse_sec_units(units)

    def _parse_sec_units(self, units: Dict[str, List[Dict]]):
        """Parses the SECUnits into a flat list of values"""
        for unit, list_of_sec_unit_info in units.items():
            for sec_unit_info in list_of_sec_unit_info:
                self.units.append(SECUnits(unit=unit, **sec_unit_info))
                self._form_type_to_unit[self.units[-1].form_type].append(self.units[-1])

    def get_by_form_type(self, form_type: str) -> Optional[List[SECUnits]]:
        """
        Returns the list of sec units for the given form type for the base measure
        :param form_type: The form type to which we want to retrieve the data e.g. 10-K for yearly report or
            10-Q for retrieving the quarterly reports.
        :return: The list of sec units when found, None otherwise
        """
        return self._form_type_to_unit.get(form_type, None)

    def to_dict(self):
        return {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "units": [unit.to_dict() for unit in self.units]
        }
