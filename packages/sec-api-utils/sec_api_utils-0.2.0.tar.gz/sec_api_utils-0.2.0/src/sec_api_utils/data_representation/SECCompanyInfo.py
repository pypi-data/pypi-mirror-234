from typing import Optional, Union, List

from ..data_representation.SECBaseMeasure import SECBaseMeasure
from ..data_representation.SECFilingInfo import SECFilingInfo


class SECCompanyInfo:
    cik: str
    company_name: str
    ticker_name: str
    facts: SECFilingInfo

    def __init__(self, cik: Union[int, str], entityName: str, facts: dict):
        self.cik = str(cik).zfill(10)
        self.company_name = entityName
        self.facts = SECFilingInfo(facts)
        self.ticker_name = ""

    def get_measure_info(self, name: str) -> Optional[SECBaseMeasure]:
        """
        Returns the measure info to the given name
        :param name: The name of the measure to extract
        :return: The SECBaseMeasure when found, None otherwise
        """
        return self.facts.get_measure_info(name)

    def set_ticker_name(self, ticker_name: str):
        self.ticker_name = ticker_name

    def to_dict(self):
        my_dict = self.__dict__
        my_dict["facts"] = self.facts.to_dict()
        return my_dict

    def measures_to_list_of_dicts(self) -> List[dict]:
        """
        Converts the SECBaseMeasure inside the SECFilingInfo into a list of SECBaseMeasures containing the company name
        and the ticker name of the company as well as the CIK number.
        """
        return self.facts.measures_to_list_of_dicts(self.company_name, self.ticker_name, self.cik)

    def get_document_entity_information_names(self) -> List[str]:
        """
        Retrieves the names from the document entity information of the SECFilingInfo of the company
        representing certain information like the NumberOfSharesOutstanding.
        :return: The names of measures, which are available for the company.
        """

        return [measure.name for measure in self.facts.document_and_entity_information]

    def get_document_entity_information_labels(self) -> List[str]:
        """
        Retrieves the labels from the document entity information of the SECFilingInfo of the company
        representing certain information like the NumberOfSharesOutstanding.
        :return: The labels of measures, which are available for the company.
        """

        return [measure.label for measure in self.facts.document_and_entity_information]
