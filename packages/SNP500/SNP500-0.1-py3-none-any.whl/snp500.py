from typing import List
import pandas as pd

class SNP500:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self._table = None
        self._tickers = None
        self._companies = None
        self._sector = None

    @property
    def table(self) -> pd.DataFrame:
        if self._table is None:
            self._table = self._get_table()
        return self._table

    @property
    def tickers(self) -> List[str]:
        if self._tickers is None:
            self._tickers = self.table["Symbol"].to_list()
        return self._tickers

    @property
    def companies(self) -> pd.DataFrame:
        if self._companies is None:
            self._companies = self.table[["Symbol", "Security"]]
        return self._companies

    @property
    def sector(self) -> pd.DataFrame:
        if self._sector is None:
            self._sector = self.table[["Symbol", "GICS Sector"]]
        return self._sector
    
    def _get_table(self) -> pd.DataFrame:
        try:
            table = pd.read_html(self._url)[0]
            table["Symbol"] = table["Symbol"].str.replace(".", "-")
            return table
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data: {e}")

    def refresh_data(self):
        self._table = self._get_table()
        self._tickers = None
        self._companies = None
        self._sector = None
