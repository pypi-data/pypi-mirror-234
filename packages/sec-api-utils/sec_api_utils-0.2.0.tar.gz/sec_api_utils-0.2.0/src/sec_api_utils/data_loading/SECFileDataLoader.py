import json
import os
import traceback
from multiprocessing import Pool, Lock
from pprint import pprint

from pymongo import MongoClient
from pymongo.collection import Collection

from ..data_representation.SECCompanyInfo import SECCompanyInfo

lock: Lock


def init_multiprocessing(multi_proc_lock: Lock):
    global lock
    lock = multi_proc_lock


def load_data(docs, path_to_filings, tickers_cik, tickers_name, start_index, end_index):
    global lock
    data_retrieved = []
    for i in range(start_index, end_index):
        print(f"\rCurrent index {i}", end="")
        company_data = json.load(open(f"{path_to_filings}/{docs[i]}"))
        if len(company_data) == 0:
            return

        try:
            company_info = SECCompanyInfo(**company_data)
            # print(f"Entity Name: {company_info.entity_name}")
            if company_info.cik in tickers_cik:
                company_info.set_ticker_name(tickers_cik[company_info.cik])
            elif company_info.company_name in tickers_name:
                company_info.set_ticker_name(tickers_name[company_info.company_name])
            else:
                pass
                # print(f"Unknown CIK {company_info.cik}")

            lock.acquire()
            data_retrieved.extend(company_info.measures_to_list_of_dicts())
            lock.release()

            # print(company_info.ticker_name)
        except Exception as e:
            lock.release()
            pprint(traceback.format_exc())

    # print(data_retrieved)
    try:
        conn = MongoClient()
        db = conn["SECData"]
        coll = db["SECInfo"]
        coll.insert_many(data_retrieved)
    except Exception:
        pprint(traceback.format_exc())
        exit()


class SECFileDataLoader:

    def __init__(self, path_to_filings: str, path_to_tickers: str, n: int, j: int = 6,
                 ip: str = "127.0.0.1", port: int = 27017, number_of_entries_per_process: int = 50):
        """
        Initializes the data loader and loads the data
        :param path_to_filings: The path to the sec filings
        :param path_to_tickers: The path to the ticker file for mapping
        :param n: The number of documents to read if -1 is passed all documents in the path_to_filings
                  directory are read
        :param j: The number of workers for reading the files.
        """
        conn = MongoClient(ip, port)
        db = conn["SECData"]
        coll = db["SECInfo"]
        coll.drop()
        coll.insert_one({"DUMMY": "DUMMY"})
        l = Lock()
        tickers = json.load(open(path_to_tickers))
        tickers_cik = {str(t["cik_str"]).zfill(10): t["ticker"] for key, t in tickers.items()}
        tickers_name = {t["title"]: t["ticker"] for key, t in tickers.items()}
        docs = os.listdir(path_to_filings)
        self.data = []
        if n == -1:
            n = len(docs)

        results = []
        with Pool(processes=j, initializer=init_multiprocessing, initargs=(l,)) as pool:
            for i in range(0, n, number_of_entries_per_process):
                if i < len(docs):
                    res = pool.apply_async(load_data,
                                           args=(docs, path_to_filings, tickers_cik, tickers_name, i,
                                                 i + number_of_entries_per_process,))
                    results.append(res)
                print(f"\rProcessed res_count {i}/{n}!", end="")

            pool.close()
            pool.join()
        print(f"Finished!")

    def mongodb_data_to_from_secinfo_to_secunits(self, coll: Collection):
        """
        Splits the SECInfo entries, which contains the SECBaseMeasures into its SECUnits. Descriptions and
        the units are placed in the root document.
        """
        coll.aggregate([
            {
                '$unwind': {
                    'path': '$units'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': {
                        '$mergeObjects': [
                            '$$ROOT', '$units'
                        ]
                    }
                }
            }, {
                '$project': {
                    'units': 0,
                    '_id': 0
                }
            }, {
                '$out': 'SECUnits'
            }
        ])
