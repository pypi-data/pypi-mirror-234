import pandas as pd
import time
from pathlib import Path
from evergreenlib.clean.cleaner import DataframeCleaner

pd.options.display.width = None


class TxtParser:
    def __init__(self, filepath: str = None, idx_value: str = None):
        self.filepath = filepath
        self.idx_value = idx_value
        self.dataframe = None

    def read_data(self):
        start = time.perf_counter()
        self.dataframe = pd.read_csv(self.filepath, encoding='cp1251', sep='\t', dtype=str)
        self.dataframe = self.dataframe.iloc[:, 0].str.split("|", expand=True)
        cleaner = DataframeCleaner(self.dataframe)
        cleaner.adj_by_row_index(value=self.idx_value)
        cleaner.remove_duplicated_cols()
        end = time.perf_counter()
        print(
            f'Reading file {Path(self.filepath).name} '
            f'from file: {Path(__file__).__fspath__()} took {round((end - start), 2)} seconds'
        )

        return cleaner.df


if __name__ == '__main__':
    x = TxtParser(
        r'V:\Findep\Incoming\test\DevOps\ARAP Project\Project\Accounting Input Data\YTD07_2023\AP07YTD2023_02Aug2023.txt',
        "Account")

    print(x.read_data())
