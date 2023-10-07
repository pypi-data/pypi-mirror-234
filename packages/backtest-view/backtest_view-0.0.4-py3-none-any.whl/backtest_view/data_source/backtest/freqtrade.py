import os
import json
import logging
import subprocess
import pandas as pd
from pathlib import Path
from typing import List, Callable
from datetime import datetime, timedelta, timezone
from backtest_view.constants import Timeframe
from backtest_view.data_source.backtest.abstract import AbstractBacktestDataSource
from backtest_view.utilities import candles_to_seconds

logger = logging.getLogger(__name__)


class FreqtradeBacktestDataSource(AbstractBacktestDataSource):

    def __init__(self, *args, **kwargs):
        super(FreqtradeBacktestDataSource, self).__init__(*args, **kwargs)
        self._set_freqtrade_envs()
        self._strategy_instance = self._get_strategy()

    @staticmethod
    def _set_freqtrade_envs():
        # todo maybe trim configs instead?
        os.environ.update({
                'FREQTRADE__EXCHANGE__KEY': '',
                'FREQTRADE__EXCHANGE__SECRET': '',
                'FREQTRADE__TELEGRAM__TOKEN': '',
                'FREQTRADE__TELEGRAM__CHAT_ID': '',
                'FREQTRADE__API_SERVER__USERNAME': '',
                'FREQTRADE__API_SERVER__PASSWORD': ''
            })

    @staticmethod
    def _get_formatted_timerange(
            start: datetime,
            end: datetime
    ):
        start_string = start.strftime('%Y%m%d')
        end_string = end.strftime('%Y%m%d')
        return f'{start_string}-{end_string}'

    def _get_config(self) -> dict:
        from freqtrade.configuration import Configuration

        # get the current working directory
        working_dir = os.getcwd()

        # freqtrade needs this as the working directory
        os.chdir(os.path.join(self.project_folder, os.pardir))

        config = Configuration.from_files([self.config])

        config["timeframe"] = self.timeframe.value
        config['strategy'] = self.strategy

        # restore current working directory
        os.chdir(working_dir)

        return config

    def _get_strategy(self) -> object:
        from freqtrade.resolvers import StrategyResolver

        # get the current working directory
        working_dir = os.getcwd()

        # freqtrade needs this as the working directory
        os.chdir(os.path.join(self.project_folder, os.pardir))

        # get the config
        config = self._get_config()

        # load the strategy
        strategy = StrategyResolver.load_strategy(config)

        # restore current working directory
        os.chdir(working_dir)

        return strategy

    def get_last_backtest_file_path(self):
        last_result_path = os.path.join(
            self.project_folder,
            'backtest_results',
            '.last_result.json'
        )
        if os.path.exists(last_result_path):
            with open(last_result_path) as last_result_path_file:
                file_name = json.load(last_result_path_file).get('latest_backtest')

            return os.path.join(
                self.project_folder,
                'backtest_results',
                file_name
            )
        else:
            raise FileNotFoundError(
                'There are no recent backtests. Please run a backtest that exports the results '
                'to the default location and try again.'
            )

    def get_trades(
            self,
            strategy: str
    ) -> dict:
        file_path = self.get_last_backtest_file_path()
        data = self.get_json_data(file_path)
        organized_trades = {}
        for trade in data['strategy'][strategy]['trades']:
            trades = organized_trades.get(trade['pair'], [])
            trades.append(trade)
            organized_trades[trade['pair']] = trades

        return organized_trades

    def get_candles(
            self,
            pair: str,
            start: datetime = datetime.now(tz=timezone.utc) - timedelta(days=90),
            end: datetime = datetime.now(tz=timezone.utc),
            timeframe: Timeframe = Timeframe.HOUR,
            download: bool = True
    ) -> pd.DataFrame:
        from freqtrade.data.history import load_pair_history

        # convert start and end to timerange string
        timerange = self._get_formatted_timerange(start, end)

        if not timeframe:
            timeframe = self.timeframe

        # download candles
        if download:
            logger.info('Downloading candles....')
            command = [
                "freqtrade",
                "download-data",
                "--config",
                self.config,
                "--timerange",
                timerange,
                "--userdir",
                self.project_folder,
                "--timeframes",
                timeframe.value,
                "--pairs",
                pair
            ]

            subprocess.run(
                command,
                env=os.environ,
                cwd=os.path.join(self.project_folder, os.pardir)
            )
            logger.info('Candle download complete!')

        config = self._get_config()

        return load_pair_history(
            datadir=Path(self.project_folder, 'data', config['exchange']['name']),
            timeframe=timeframe.value,
            pair=pair
        )

    def get_evaluated_strategy(
            self,
            pair: str,
            start: datetime = datetime.now(tz=timezone.utc) - timedelta(days=90),
            end: datetime = datetime.now(tz=timezone.utc),
            timeframe: Timeframe = Timeframe.HOUR,
            download: bool = True
    ) -> pd.DataFrame:
        from freqtrade.data.dataprovider import DataProvider
        candles = self.get_candles(
            pair=pair,
            start=start,
            end=end,
            timeframe=timeframe,
            download=download
        )
        config = self._get_config()
        strategy = self._get_strategy()

        # Todo do we need to provide exchange?
        strategy.dp = DataProvider(config=config, exchange=None)
        strategy.ft_bot_start()

        # Generate buy/sell signals using strategy
        return strategy.analyze_ticker(candles, {'pair': pair})

    def get_startup_time_delta(self) -> pd.Timedelta:
        seconds = candles_to_seconds(
            self._strategy_instance.startup_candle_count,
            self.timeframe.value
        )
        return pd.Timedelta(seconds=seconds)

    def get_replay_config_callback(self) -> Callable:
        return self._strategy_instance.get_replay_config

    def _normalize_trade_format(
            self,
            trades: List[dict]
    ) -> List[dict]:
        return trades
