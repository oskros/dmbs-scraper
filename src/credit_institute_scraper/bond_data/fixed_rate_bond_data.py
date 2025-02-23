import pandas as pd
from .fixed_rate_bond_data_entry import FixedRateBondDataEntry


class FixedRateBondData:
    def __init__(self, fixed_rate_bond_data_entries: list[FixedRateBondDataEntry]):
        self.fixed_rate_bond_data_entries = fixed_rate_bond_data_entries

    def to_pandas_data_frame(self, scrape_time):
        df = pd.DataFrame.from_dict([x.__dict__ for x in self.fixed_rate_bond_data_entries])
        df.insert(0, "timestamp", scrape_time)

        return df
