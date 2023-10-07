import json
from typing import Dict, List

COMPANY_NAME_TO_CIK = "company_name_to_cik"
TICKER_TO_CIK = "ticker_to_cik"

API_STRUCTURE_FIELD_TICKER = "ticker"
API_STRUCTURE_FIELD_TITLE = "title"
API_STRUCTURE_FIELD_CIK = "cik_str"


class CompanyTickerHandler:
    company_name_to_cik: Dict[str, int]
    ticker_to_cik: Dict[str, int]

    def __init__(self, company_tickers_json: dict):
        self.company_name_to_cik = {}
        self.ticker_to_cik = {}

        if '0' in company_tickers_json.keys():
            self.load_from_sec_api_structure(company_tickers_json)
        elif COMPANY_NAME_TO_CIK in company_tickers_json and TICKER_TO_CIK in company_tickers_json:
            self.load_from_file_structure(company_tickers_json)
        else:
            raise ValueError("Unknown format for company tickers JSON")

    def load_from_file_structure(self, company_tickers_json: dict):
        """
        Loads the json from the file structure rather than the api structure
        :param company_tickers_json: The json file to load into the handler
        """
        self.company_name_to_cik = company_tickers_json[COMPANY_NAME_TO_CIK]
        self.ticker_to_cik = company_tickers_json[TICKER_TO_CIK]

    def load_from_sec_api_structure(self, company_tickers_json: dict):
        """
        Loads the json from the api structure into the correct lookup tables
        :param company_tickers_json: The json file to load into the handler
        """
        for _, company_tick_info in company_tickers_json.items():
            cik = company_tick_info[API_STRUCTURE_FIELD_CIK]
            title = company_tick_info[API_STRUCTURE_FIELD_CIK]
            ticker = company_tick_info[API_STRUCTURE_FIELD_TICKER]
            if isinstance(cik, int) or len(cik) > 0:
                self.company_name_to_cik[title] = int(cik)
                self.ticker_to_cik[ticker] = int(cik)

    def store_company_tickers_to_file(self, filepath: str):
        """
        Store the company tickers loaded into the file to the given path
        :param filepath: The path to the file where to store the loaded tickers.
        """
        fd = open(filepath, "w+")
        ticker_dump = {
            COMPANY_NAME_TO_CIK: self.company_name_to_cik,
            TICKER_TO_CIK: self.ticker_to_cik
        }
        fd.write(json.dumps(ticker_dump))

    def get_cik_to_ticker(self, ticker_name: str) -> int:
        """
        Returns the CIK to the ticker name
        :param ticker_name: The ticker name for which we want to know the CIK number
        :return: The CIK retrieved.
        """
        return self.ticker_to_cik[ticker_name]

    def get_cik_to_company_name(self, company_name: str) -> List[int]:
        """
        Returns the CIK numbers all names matching the company name query
        :param company_name: The company name query for which we want to know the CIK numbers.
        :return: The CIK retrieved.
        """
        raise NotImplementedError("Retrieving the cik to the company name is currently not supported")
