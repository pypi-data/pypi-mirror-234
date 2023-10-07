
import json
import os
from typing import List
from abc import abstractmethod
from backtest_view.constants import FileFormats
from backtest_view.data_source.abstract import AbstractDataSource


class AbstractBacktestDataSource(AbstractDataSource):
    @classmethod
    def get_json_data(
            cls,
            file_path: str
    ) -> dict:
        if os.path.exists(file_path):
            with open(file_path) as file:
                return json.load(file)
        return {}

    @classmethod
    def get_backtest_data(
            cls,
            path: str,
            file_format: FileFormats = FileFormats.JSON
    ) -> dict:
        if file_format == FileFormats.JSON:
            cls.get_json_data(path)
        return {}

    @abstractmethod
    def get_last_backtest_file_path(self) -> str:
        raise NotImplementedError
