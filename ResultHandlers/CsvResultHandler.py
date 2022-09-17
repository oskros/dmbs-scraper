import os
import pandas as pd
from datetime import datetime

from FixedRateBond import FixedRateBond
from ResultHandlers.ResultHandler import ResultHandler


class CsvResultHandler(ResultHandler):
    def __init__(self, scrape_time: datetime):
        self.scrape_time = scrape_time

    def result_exists(self):
        return os.path.exists(self.csv_path)

    def export_result(self, result: list[FixedRateBond]):
        if not os.path.exists(self.day_path):
            os.makedirs(self.day_path)

        pd.DataFrame.from_dict([x.__dict__ for x in result]).to_csv(self.csv_path, index=False)

    @property
    def csv_path(self):
        return f"{self.day_path}/{self.scrape_time.strftime('%Y%m%d%H%M')}.csv"

    @property
    def day_path(self):
        return f"./Kurser/{self.scrape_time.strftime('%Y%m%d')}"
