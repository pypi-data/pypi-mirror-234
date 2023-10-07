import logging
import asyncio
import numpy as np
import pandas as pd
from time import sleep
from typing import List
from backtest_view.constants import PlotType, Timeframe
from lightweight_charts import Chart, JupyterChart
from backtest_view.utilities import within_timestamp, candles_to_seconds
from backtest_view.data_source.abstract import AbstractDataSource


logger = logging.getLogger(__name__)


class Plot:
    def __init__(
            self,
            data_sources: List[AbstractDataSource],
            timeframe: Timeframe,
            replay: bool = False,
            show_subplots: bool = True,
            candle_plot_scale: int = 3,
            redraw_interval: float = 0.01,
            width: int = 800,
            height: int = 350
    ):
        self._data_sources = data_sources
        self._timeframe = timeframe
        self._replay = replay
        self._show_subplots = show_subplots
        self._candle_plot_scale = candle_plot_scale
        self._redraw_interval = redraw_interval

        self._references = {}
        self._dataframes = {}
        self._chart = None
        self._sub_plot_height = None
        self._candle_plot_height = None
        self._current_trade_index = {}
        self._notebook_chart_kwargs = {
            'width': width,
            'height': height
        }

        # event variables
        self._paused = False
        self._current_time_index = 0

        # validate
        self._validate()

        # initialize data
        self._create_main_chart()
        self._set_dataframes()

    def _validate(self):
        if self.in_notebook and self._replay:
            raise ValueError(
                f'The `replay` flag is {self._replay}, but this is in a notebook environment. The replay feature is not available in a notebook.'
                )

    def _create_main_chart(self):
        num_candle_plots = 0
        num_sub_plots = 0
        for data_source in self._data_sources:
            # calculate height making room for subplots
            num_candle_plots += len(data_source.replay_config.get(PlotType.CANDLE_PLOTS.value, []))
            num_sub_plots += len(data_source.replay_config.get(PlotType.SUB_PLOTS.value, []))

        if self._show_subplots:
            self._sub_plot_height = 1 / (num_sub_plots + (num_candle_plots * self._candle_plot_scale))
            self._candle_plot_height = self._sub_plot_height * self._candle_plot_scale
        else:
            self._sub_plot_height = 0
            self._candle_plot_height = 1 / num_candle_plots

        # switch chart class and kwargs if this is run in a notebook
        chart_class = Chart
        kwargs = {
            'inner_width': 1, 
            'inner_height': self._candle_plot_height
            }

        if self.in_notebook:
            chart_class = JupyterChart
            kwargs.update(self._notebook_chart_kwargs)

        self._chart = chart_class(**kwargs)

    def _set_dataframes(self):
        for data_source in self._data_sources:
            self._dataframes[data_source.name] = self._dataframes.get(data_source.name, {})

            for pair, dataframe in data_source.dataframes.items():
                # get the time range to show based on the trades
                time_range = dataframe[(
                    dataframe['date'] > self.first_trade_open - self.startup_time_delta) & (
                    dataframe['date'] < self.last_trade_close)]

                # if replay is off then initialize the chart with all candles
                if not self._replay:
                    initial_dataframe, replay_dataframe = np.split(time_range, [-1], axis=0)

                else:
                    # if replay is on then initialize the chart with only the first candle
                    initial_dataframe, replay_dataframe = np.split(time_range, [1], axis=0)

                self._dataframes[data_source.name][pair] = {
                    'initial_dataframe': initial_dataframe,
                    'replay_dataframe': replay_dataframe,
                }

    def _get_timestamps(self) -> pd.DatetimeIndex:
        return pd.period_range(
            start=self.first_trade_open - self.startup_time_delta + pd.Timedelta(
                seconds=candles_to_seconds(
                    count=2,
                    timeframe=self._timeframe.value
                )
            ),
            end=self.last_trade_close,
            freq=self._timeframe.value[-1]
        ).to_timestamp().tz_localize('utc')

    @property
    def in_notebook(self) -> bool:
        try:
            from IPython import get_ipython
            if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
                return False
        except ImportError:
            return False
        except AttributeError:
            return False
        return True

    @property
    def startup_time_delta(self) -> pd.Timedelta:
        largest_delta = None
        for data_source in self._data_sources:
            if not largest_delta or data_source.startup_time_delta > largest_delta:
                largest_delta = data_source.startup_time_delta
        return largest_delta

    @property
    def first_trade_open(self) -> pd.Timestamp:
        first_trade = None
        for data_source in self._data_sources:
            if data_source.trades:
                for pair, trades in data_source.trades.items():
                    open_date = pd.Timestamp(trades[0]['open_date'])
                    if not first_trade or open_date < first_trade:
                        first_trade = open_date
        return first_trade

    @property
    def last_trade_close(self) -> pd.Timestamp:
        last_trade = None
        for data_source in self._data_sources:
            if data_source.trades:
                for pair, trades in data_source.trades.items():
                    close_date = pd.Timestamp(trades[-1]['close_date'])
                    if not last_trade or close_date > last_trade:
                        last_trade = close_date
        return last_trade

    @staticmethod
    def line_update(
            series: pd.Series,
            name: str,
    ) -> pd.Series:
        return pd.Series({
            'time': series['date'],
            name: series[name]
        })

    @staticmethod
    def line_init(
            dataframe: pd.DataFrame,
            name: str
    ) -> pd.DataFrame:
        return pd.DataFrame({
            'time': dataframe['date'],
            name: dataframe[name]
        })

    @staticmethod
    def candle_update(
            series: pd.Series
    ) -> pd.Series:
        return pd.Series({
            'date': series[f'date'],
            'open': series[f'open'],
            'close': series[f'close'],
            'high': series[f'high'],
            'low': series[f'low']
        })

    @staticmethod
    def candle_init(
            dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        return pd.DataFrame({
            'date': dataframe[f'date'],
            'open': dataframe[f'open'],
            'close': dataframe[f'close'],
            'high': dataframe[f'high'],
            'low': dataframe[f'low']
        })

    def _set_candle_plot(
            self,
            plot_type: PlotType,
            plot_index: int,
            references: dict,
            dataframe: pd.DataFrame
    ) -> dict:
        # the first candle plot is the main chart
        if plot_type == PlotType.CANDLE_PLOTS and plot_index == 0:
            references['chart'] = self._chart
        # if this is the second candle plot or a subplot assign it a new chart
        else:
            # get the correct plot height
            chart_height = self._candle_plot_height
            if plot_type == PlotType.SUB_PLOTS:
                chart_height = self._sub_plot_height

            references['chart'] = self._chart.create_subchart(
                width=1,
                height=chart_height,
                sync=True
            )

        # set the candles if this is a candle plot
        if plot_type == PlotType.CANDLE_PLOTS:
            references['chart'].set(self.candle_init(dataframe))

        return references

    def _set_line_plot(
            self,
            data: dict,
            references: dict,
            dataframe: pd.DataFrame
    ) -> dict:
        lines = data.get('lines')
        if lines:
            references['lines'] = []
            for line_name, line_data in lines.items():
                # create the line instance
                line_instance = references['chart'].create_line(
                    line_name,
                    **{key: value for key, value in line_data.items()}
                )
                # populate it's data
                line_instance.set(
                    self.line_init(
                        dataframe=dataframe,
                        name=line_name
                    )
                )
                # save the reference to the line instance
                references['lines'].append(line_instance)
        return references

    @staticmethod
    def _set_markers_plot(
            data: dict,
            references: dict,
            dataframe: pd.DataFrame
    ) -> dict:
        markers = data.get('markers')
        if markers:
            chart = references['chart']
            for marker_name, marker_data in markers.items():
                for index, series in dataframe.iterrows():
                    timestamp = series['date']
                    value = series[marker_name]
                    display_settings = marker_data.get(value)

                    if display_settings:
                        chart.marker(
                            time=timestamp,
                            text=display_settings.get('text'),
                            position=display_settings.get('position'),
                            shape=display_settings.get('shape'),
                            color=display_settings.get('color'),
                        )

        return references

    def init_plots(self, plot_type: PlotType):
        for data_source in self._data_sources:
            self._references[data_source.name] = self._references.get(data_source.name, {})
            for index, data in enumerate(data_source.replay_config[plot_type.value]):
                references = {}
                # subplots don't need a specific pair since they should already be part of the dataframe
                default_pair = data_source.pair if plot_type == PlotType.SUB_PLOTS else None

                # candle plots must specify a pair
                pair = data.get('pair', default_pair)

                dataframe = self._dataframes[data_source.name][pair]['initial_dataframe']
                self._references[data_source.name][pair] = self._references[data_source.name].get(pair, {})

                # set candle plot
                references = self._set_candle_plot(
                    plot_type=plot_type,
                    plot_index=index,
                    references=references,
                    dataframe=dataframe
                )

                # set the lines
                references = self._set_line_plot(
                    data=data,
                    references=references,
                    dataframe=dataframe
                )

                # set the markers
                references = self._set_markers_plot(
                    data=data,
                    references=references,
                    dataframe=dataframe
                )

                # set the watermark
                watermark = data.get('watermark')
                if watermark:
                    references['chart'].watermark(text=watermark)

                # initialize the plot index
                self._references[data_source.name][pair][plot_type.value] = self._references[data_source.name][pair].get(
                    plot_type.value, {}
                )

                # save all references for this candle plot
                self._references[data_source.name][pair][plot_type.value][index] = references

    def set_trade(self, data_source: AbstractDataSource, timestamp: pd.Timestamp):
        plot_type = PlotType.CANDLE_PLOTS.value

        for index, candle_plot in enumerate(data_source.replay_config[plot_type]):
            pair = candle_plot['pair']

            trades = data_source.trades.get(pair)
            if trades:
                trade_index = self._current_trade_index.get(pair, 0)
                if trade_index < len(data_source.trades[pair]):
                    trade = data_source.trades[pair][trade_index]
                    trade_pair = trade['pair']
                    trade_start_date = pd.Timestamp(trade['open_date'])
                    trade_end_date = pd.Timestamp(trade['close_date'])
                    trade_profit = trade['profit_abs']
                    trade_exit_reason = trade['exit_reason']
                    trade_amount = trade['amount']
                    trade_open_rate = trade['open_rate']
                    trade_close_rate = trade['close_rate']
                    trade_initial_stop_loss = trade['initial_stop_loss_abs']

                    chart = self._references[data_source.name][pair][plot_type][index]['chart']

                    # if there is no existing stoploss line
                    stoploss = self._references[data_source.name][pair][plot_type][index].get('stoploss')
                    if not stoploss:
                        # create a stoploss line
                        self._references[data_source.name][pair][plot_type][index]['stoploss'] = chart.create_line(
                            'stoploss',
                            color='red',
                            style='sparse_dotted'
                        )

                    if within_timestamp(timestamp, trade_start_date, timeframe=self._timeframe):
                        chart.marker(
                            time=timestamp,
                            text=f'Entered ${trade_amount * trade_open_rate} {trade_pair}',
                            position='below',
                            shape='arrow_up',
                            color='#18FFFF'
                        )
                    if within_timestamp(timestamp, trade_end_date, timeframe=self._timeframe):
                        color = 'rgb(76, 175, 80)' if trade_profit > 0 else '#FF3D00'
                        prefix = '$' if trade_profit > 0 else '-$'
                        chart.marker(
                            time=timestamp,
                            text=f'Exited ${trade_amount * trade_close_rate} {trade_pair} Profit: {prefix}{abs(trade_profit)}',
                            position='above',
                            shape='arrow_down',
                            color=color
                        )
                        trade_index += 1
                        self._current_trade_index[pair] = trade_index

    def init_trades(self):
        # skip adding trades if replay is on since they will be added in by the updates
        if self._replay:
            return

        # set trades from all data sources
        for data_source in self._data_sources:
            dataframe = self._dataframes[data_source.name][data_source.pair]['initial_dataframe']
            for _, series in dataframe.iterrows():
                self.set_trade(data_source, series['date'])

    def update_plots(self, data_source: AbstractDataSource, timestamp: pd.Timestamp, plot_type: PlotType):
        # indicators
        for index, data in enumerate(data_source.replay_config[plot_type.value]):
            # subplots don't need a specific pair since they should already be part of the dataframe
            default_pair = data_source.pair if plot_type == PlotType.SUB_PLOTS else None

            # candle plots must specify a pair
            pair = data.get('pair', default_pair)
            dataframe = self._dataframes[data_source.name][pair]['replay_dataframe']
            series = dataframe.loc[dataframe['date'] == timestamp].iloc[-1]
            chart = self._references[data_source.name][pair][plot_type.value][index]['chart']

            # update candles if this is a candle plot
            if plot_type == PlotType.CANDLE_PLOTS:
                candle = self.candle_update(series)
                chart.update(candle)

            # update lines
            for line_index, line_name in enumerate(data.get('lines', {}).keys()):
                point = self.line_update(
                    series,
                    name=line_name
                )
                self._references[data_source.name][pair][plot_type.value][index]['lines'][line_index].update(point)

            # update markers
            for marker_name, marker_data in data.get('markers', {}).items():
                value = series[marker_name]
                display_settings = marker_data.get(value)

                if display_settings:
                    chart.marker(
                        time=timestamp,
                        text=display_settings.get('text'),
                        position=display_settings.get('position'),
                        shape=display_settings.get('shape'),
                        color=display_settings.get('color')
                    )

    def _update_plot(self, data_source: AbstractDataSource, timestamp: pd.Timestamp):
        self.update_plots(data_source, timestamp, plot_type=PlotType.CANDLE_PLOTS)
        self.set_trade(data_source, timestamp)

        if self._show_subplots:
            self.update_plots(data_source, timestamp, plot_type=PlotType.SUB_PLOTS)

        sleep(self._redraw_interval)

    def _update(self, timestamp: pd.Timestamp):
        for data_source in self._data_sources:
            self.loop(data_source, timestamp)
            self._update_plot(data_source, timestamp)

    async def _start_loop(self):
        for index, timestamp in enumerate(self._get_timestamps()):

            # holds here if paused is true
            while self._paused:
                # update the plot if the current time index changes
                # this could be from the forward arrow
                if self._current_time_index >= index:
                    break

                await asyncio.sleep(self._redraw_interval)

            self._update(timestamp)
            self._current_time_index = index
            await asyncio.sleep(self._redraw_interval)

    def _set_events(self):
        logger.debug('Setting events...')
        self._chart.hotkey(None, ' ', self._pause_event)
        self._chart.hotkey(None, 'ArrowRight', self._move_forward_event)

    def _pause_event(self, key):
        self._paused = not self._paused

        if self._paused:
            logger.info('Paused.')
        else:
            logger.info('Playing.')

    def _move_forward_event(self, key):
        self._current_time_index += 1
        logger.info(f'Moving time index forward to {self._current_time_index}.')

    def show(self):
        self.init_plots(plot_type=PlotType.CANDLE_PLOTS)
        self.init_trades()
        self._set_events()

        if self._show_subplots:
            self.init_plots(plot_type=PlotType.SUB_PLOTS)

        # if replay is on
        if self._replay:
            asyncio.run(self.replay())
        else:
            # load the chart correctly if in a notebook
            if self.in_notebook:
                self._chart.load()
            else:
                self._chart.show(block=True)

    async def replay(self):
        # if replay is on
        await asyncio.gather(
            self._chart.show_async(block=True),
            self._start_loop()
        )

    def loop(self, data_source: AbstractDataSource, timestamp: pd.Timestamp):
        """
        This can be overriden if you want to define your own logic within the loop.
        """
        pass
