from pprint import pformat, pprint
from typing import List, Dict, Optional

from ..data_representation.SECBaseMeasure import SECBaseMeasure
from ..general.SECConstants import DEI_API_FIELD, US_MINUS_GAAP_API_FIELD, SRT_FIELD, \
    IFRS_MINUS_FULL_API_FIELD, INVEST_FIELD, DOCUMENT_AND_ENTITY_INFORMATION_FIELD, US_GAAP_FIELD, COMPANY_NAME_FIELD, \
    TICKER_NAME_FIELD, CIK_FIELD, IFRS_FULL_FIELD


class SECFilingInfo:
    document_and_entity_information: List[SECBaseMeasure]
    us_gaap: List[SECBaseMeasure]
    srt: List[SECBaseMeasure]
    invest: List[SECBaseMeasure]
    ifrs_full: List[SECBaseMeasure]
    _base_measure_map: Dict[str, SECBaseMeasure]

    def __repr__(self):
        return pformat(self.__dict__)

    def _process_base_measures(self, data: dict, key: str, delete_key: bool = True):
        """
        Retrieves a base measure from the data dictionary based on the given key and creates the corresponding objects.
        Also fills the lookup map for base measures
        :param data: Data dictionary containing information about the companies filings
        :param key: The key which should be extracted and converted to base measures
        :param delete_key: If true the key and value for the key are deleted from the data dictionary
        """
        if key in data:
            for base_measure_name, base_measure_entry in data[key].items():
                sec_base_measure = SECBaseMeasure(base_measure_name, **base_measure_entry)
                self.document_and_entity_information.append(sec_base_measure)
                self._base_measure_map[base_measure_name] = sec_base_measure

            if delete_key:
                data.pop(key)

    def __init__(self, data: dict):
        self.document_and_entity_information = []
        self.us_gaap = []
        self.srt = []
        self.invest = []
        self.ifrs_full = []
        self._base_measure_map = {}
        self._process_base_measures(data, DEI_API_FIELD, delete_key=True)
        self._process_base_measures(data, US_MINUS_GAAP_API_FIELD, delete_key=True)

        if SRT_FIELD in data.keys():
            self._process_base_measures(data, SRT_FIELD, delete_key=True)
        if IFRS_MINUS_FULL_API_FIELD in data.keys():
            self._process_base_measures(data, IFRS_MINUS_FULL_API_FIELD, delete_key=True)
        if INVEST_FIELD in data.keys():
            self._process_base_measures(data, INVEST_FIELD, delete_key=True)

        pprint(self._base_measure_map.keys())

        if len(data) > 0:
            print(f"Unknown keys {data.keys()} in object")

    def get_measure_info(self, name: str) -> Optional[SECBaseMeasure]:
        """
        Returns the measure info to the given name
        :param name: The name of the measure to extract
        :return: The SECBaseMeasure when found, None otherwise
        """
        return self._base_measure_map.get(name, None)

    def to_dict(self):
        return {
            DOCUMENT_AND_ENTITY_INFORMATION_FIELD: [x.to_dict() for x in self.document_and_entity_information],
            US_GAAP_FIELD: [x.to_dict() for x in self.us_gaap],
            SRT_FIELD: [x.to_dict() for x in self.srt],
            INVEST_FIELD: [x.to_dict() for x in self.invest],
            IFRS_FULL_FIELD: [x.to_dict() for x in self.ifrs_full],
        }

    def measures_to_list_of_dicts(self, company_name: str, ticker_name: str, cik: str) -> List[dict]:
        """
        Converts the SECBaseMeasure inside the SECFilingInfo into a list of SECBaseMeasures containing the company name
        and the ticker name of the company as well as the CIK number
        :param company_name: The name of the company
        :param ticker_name: The ticker name of the company
        :param cik: The cik number as a string with leading zeros
        :return: List of dicts containing the base measures.
        """
        company_info = {COMPANY_NAME_FIELD: company_name, TICKER_NAME_FIELD: ticker_name, CIK_FIELD: cik}
        base_measure = []
        base_measure.extend([{**company_info, **x.to_dict()} for x in self.document_and_entity_information])
        base_measure.extend([{**company_info, **x.to_dict()} for x in self.us_gaap])
        base_measure.extend([{**company_info, **x.to_dict()} for x in self.srt])
        base_measure.extend([{**company_info, **x.to_dict()} for x in self.invest])
        base_measure.extend([{**company_info, **x.to_dict()} for x in self.ifrs_full])
        return base_measure
