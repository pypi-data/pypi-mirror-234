import pandas


class Connector:

    def __init__(self):
        super().__init__()

    def init(self, info: dict):
        self.__dict__.update(info)
        return self

    def read_as_data_frame(self, table_name: str = "") -> pandas.DataFrame:
        pass

    def write_data_frame(self, df: pandas.DataFrame, table_name: str = "") -> None:
        pass

    def cached_file(self):
        raise Exception("Not Implement yet.")
