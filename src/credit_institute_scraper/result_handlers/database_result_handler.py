import pandas as pd

from ..database.sqlite_conn import query_db, client_factory
from ..result_handlers.result_handler import ResultHandler


class DatabaseResultHandler(ResultHandler):
    def __init__(self, table_name, *args, **kwargs):
        self._table_name = table_name
        super().__init__(*args,  **kwargs)

    def export_result(self, result_df: pd.DataFrame) -> None:
        with client_factory() as conn:
            result_df.to_sql(name=self.table_name, con=conn, if_exists='append', index=False)

    def result_exists(self) -> bool:
        result = query_db(f"select * from {self.table_name} where timestamp = '{self.scrape_time}'")
        return not result.empty

    @property
    def database_path(self):
        return "./database.db"

    @property
    def table_name(self):
        return self._table_name

