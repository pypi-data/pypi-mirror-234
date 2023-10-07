import json
import os
import time
from time import perf_counter_ns
from typing import Union, Any, List, Dict

import requests

from ..data_loading.CompanyTickerHandler import CompanyTickerHandler
from ..data_representation.SECCompanyInfo import SECCompanyInfo

CACHE_DIRECTORY = "SECAPICache"
COMPANY_TICKERS_FILE_NAME = "company_tickers.json"


class SECAPILoader:
    company_tickers_url: str
    data_api_url_format: str
    company_facts_url_format: str
    request_headers: dict
    ticker_handler: CompanyTickerHandler
    _last_access_time: int

    def __init__(self,
                 your_company_name: str,
                 your_company_email: str,
                 company_tickers_url: str = r"https://www.sec.gov/files/company_tickers.json",
                 data_api_url_format: str = "https://data.sec.gov/submissions/CIK{:010d}.json",
                 company_facts_url_format: str = "https://data.sec.gov/api/xbrl/companyfacts/CIK{:010d}.json",
                 override_cached_company_tickers: bool = False):
        """
        Initializes the api loader responsible for retrieving the data over the SEC-Api. To fit the fair use rules
        of the SEC you need to provide your name and email address as user agent
        :param company_tickers_url: The company tickers url, which contains a JSON-file with ticker name,
            CIK number and the company name. This JSON is responsible for mapping ticker names or company names to
            CIK numbers for fetching
        :param data_api_url_format: The format string representing the data url, which should be used for retrieval
            of data over the SEC api
        :param override_cached_company_tickers: Overrides company tickers stored locally, by reloading them on init
            of the api loader with the json given by company_tickers_url.
        """
        self.request_headers = {
            'User-Agent': your_company_name,
            'From': your_company_email,
            "Accept-Encoding": "gzip, deflate",
            "Host": "data.sec.gov"
        }
        self._last_access_time = 0
        self.company_tickers_url = company_tickers_url
        self.data_api_url_format = data_api_url_format
        self.company_facts_url_format = company_facts_url_format

        if not os.path.exists(CACHE_DIRECTORY):
            os.mkdir(CACHE_DIRECTORY)

        if override_cached_company_tickers or (COMPANY_TICKERS_FILE_NAME not in os.listdir(CACHE_DIRECTORY)):
            # Load the tickers from the url
            response = requests.post(self.company_tickers_url, headers=self.request_headers)

            if not response.ok:
                raise Exception("Not able to load the company tickers over the SEC-Api. "
                                f"Reason: {response.reason}, Status Code: {response.status_code}\n"
                                f"Response Text: \n{response.text}")

            self.ticker_handler = CompanyTickerHandler(json.loads(response.text))
            self.ticker_handler.store_company_tickers_to_file(f"{CACHE_DIRECTORY}/{COMPANY_TICKERS_FILE_NAME}")
        else:
            tickers_json = json.load(open(f"{CACHE_DIRECTORY}/{COMPANY_TICKERS_FILE_NAME}", "r"))
            self.ticker_handler = CompanyTickerHandler(tickers_json)

    def _handle_fair_use_rate_limit(self, limit_per_second: int = 10):
        current_time = perf_counter_ns()
        # Calc delta in seconds
        delta = (current_time - self._last_access_time) / 10 ** 9
        time_until_next_call = 1 / limit_per_second

        if delta < time_until_next_call:
            time.sleep(time_until_next_call - delta)
        self._last_access_time = current_time

    def _retrieve_from_api_with_ticker(self, ticker_name: str, format_url: str) -> dict:
        """
        Retrieves the data from the given format url by fetching via ticker name and CIK
        :param ticker_name: The ticker name to retrieve
        :param format_url: The format url to use for fetching
        :return: The data as dict.
        """

        cik = self.ticker_handler.get_cik_to_ticker(ticker_name)
        data_url = format_url.format(cik)
        self._handle_fair_use_rate_limit()
        response = requests.get(data_url, headers=self.request_headers)

        if response.ok:
            data = response.json()
        else:
            raise ConnectionError(f"Retrieved error code {response.status_code} with message {response.text} "
                                  f"while retrieving data for ticker {ticker_name} resulting in "
                                  f"api url: {data_url}")

        return data

    def get_data_from_ticker(self, ticker_name: str, as_dict: bool = False) -> Union[Any, dict]:
        """
        TODO define a class holding the filings
        Get the data either as raw dict or as classes
        :param ticker_name: The name of the ticker to retrieve
        :param as_dict: If true the data is returned as dict instead of SECCompanyInfo object.
        :return: The company info retrieved.
        """
        return self._retrieve_from_api_with_ticker(ticker_name, self.data_api_url_format)

    def get_company_facts_by_ticker(self, ticker_name: str, as_dict: bool = False):
        """
        Get the data either as raw dict or as classes
        :param ticker_name: The name of the ticker to retrieve
        :param as_dict: If true the data is returned as dict instead of SECCompanyInfo object.
        :return: The company info retrieved.
        """

        data = self._retrieve_from_api_with_ticker(ticker_name, self.company_facts_url_format)
        if as_dict:
            return data

        return SECCompanyInfo(**data)

    def get_company_facts_by_ticker_list(self, ticker_list: List[str],
                                         as_dict: bool = False) -> Dict[str, Union[SECCompanyInfo, dict]]:
        """
        Retrieves company facts by a list of tickers passed
        :param ticker_list: The list of tickers to retrieve
        :param as_dict: If true the data is returned as dictionary, otherwise each company info is converted
            to a SECCompanyInfo object
        :return: A dictionary with the ticker names as key and the SECCompanyInfo or dictionaries of data as values
        """
        result_dict = {}

        for ticker_name in ticker_list:
            result_dict[ticker_name] = self.get_company_facts_by_ticker(ticker_name, as_dict)

        return result_dict
