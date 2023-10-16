import logging
from datetime import datetime, timedelta
from typing import Optional  # for type hinting

from pandas import DataFrame, RangeIndex, Timestamp, concat

from .flow_analyser import AnalysisDetails, FlowAnalyser
from .helpers import to_bitrate
from .plotting.generic_chart import GenericChart


class BufferAnalyser(FlowAnalyser):
    """Analyse a video buffer over time.

    The analyser provides buffer state, incoming and outgoing data
    over time. It analyses the initial wait time for the video to start
    playing out.

    This analyser is intended for use with a :class:`~.traffic.VideoFlow`.

    Supports:

    * Analysis of a single flow

    .. warning::
       Does not support aggregation data from multiple flows
       (via :class:`~.analysis.AnalyserAggregator`).
    """

    # TODO - Cleanup code and define slots
    # __slots__ = (
    # )

    container_id = 0

    def __init__(
        self,
        buffer_size: int,
        play_goal_size: int,
        max_initial_wait_time: timedelta = timedelta(seconds=5),
    ) -> None:
        """Create the video buffer over time analyser.

        :param buffer_size: Size of the video buffer in Bytes.
        :type buffer_size: int
        :param play_goal_size:
           .. todo::
              Provide documentation for this parameter.
        :type play_goal_size: int
        :param max_initial_wait_time: Maximum allowed time to wait until
           the video starts to play, defaults to timedelta(seconds=5)
        :type max_initial_wait_time: timedelta, optional
        """
        super().__init__('Buffer analyser')
        self.buffer_size_max = buffer_size
        self.buffer_size: int = 0
        self.buffer_filled: int = 0
        self.buffer_consumed: int = 0
        # We can only consume if the buffer has reached a certain level.
        if not play_goal_size:
            self.buffer_consumable = True
        else:
            self.buffer_consumable = False
        self.play_goal_size = play_goal_size
        self.gap_start: Optional[Timestamp] = None
        self.df_buffer = DataFrame(
            columns=[
                "Buffer state",
                "Buffer incoming",
                "Buffer outgoing",
            ]
        )
        self.df_buffer_gap = DataFrame(columns=["Start", "Stop"])
        # Stats about the initial start time
        self.test_start: Optional[datetime] = None
        self.play_start: Optional[datetime] = None
        self.max_initial_wait_time = max_initial_wait_time
        self._log = ''

    def _initialize(self) -> None:
        # Nothing to do
        pass

    def process(self) -> None:
        # if self.buffer_size == 0:
        #     # Buffer is empty!
        #     if self.gap_start is None:
        #         self.gap_start = datetime.utcnow()
        #         self._set_result(False)
        #         self._add_failure_cause(failure_cause)
        #     else:
        #         if self.gap_start is not None:
        #             df_buffer_gap_update = DataFrame(
        #                 {
        #                     "Start": self.gap_start,
        #                     "Stop": datetime.utcnow()
        #                 }
        #             )
        #             # Avoid FutureWarning:
        #             #   The behavior of DataFrame concatenation with empty
        #             #   or all-NA entries is deprecated. In a future version,
        #             #   this will no longer exclude empty or all-NA columns
        #             #   when determining the result dtypes. To retain the
        #             #   old behavior, exclude the relevant entries before
        #             #   the concat operation.
        #             if self.df_buffer_gap.empty:
        #                 self.df_buffer_gap = df_buffer_gap_update
        #             else:
        #                 self.df_buffer_gap = concat(
        #                     [self.df_buffer_gap, df_buffer_gap_update],
        #                     ignore_index=True,
        #                 )
        #             self.gap_start = None
        if self.test_start is None:
            self.test_start = datetime.utcnow()

    def updatestats(self) -> None:
        logging.debug(
            "Buffer size: %s, filled %s, consumed %s", self.buffer_size,
            self.buffer_filled, self.buffer_consumed
        )
        self.df_buffer.loc[datetime.utcnow()] = [
            self.buffer_size,
            self.buffer_filled,
            self.buffer_consumed,
        ]
        self.buffer_filled = 0
        self.buffer_consumed = 0

    def buffer_fill(self, size: int) -> None:
        logging.debug(
            "Filling buffer of size %s with size %s", self.buffer_size, size
        )
        previous = self.buffer_size
        self.buffer_size += size
        if self.buffer_size > self.buffer_size_max:
            self.buffer_size = self.buffer_size_max
        self.buffer_filled += self.buffer_size - previous
        if not self.buffer_consumable:
            if self.buffer_size > self.play_goal_size:
                if self.play_start is None:
                    self.play_start = datetime.utcnow()
                self.buffer_consumable = True
                if self.gap_start is not None:
                    df_buffer_gap_update = DataFrame(
                        data={
                            "Start": self.gap_start,
                            "Stop": Timestamp.utcnow(),
                        },
                        index=RangeIndex(start=0, stop=1),
                    )
                    # Avoid FutureWarning:
                    #   The behavior of DataFrame concatenation with empty
                    #   or all-NA entries is deprecated. In a future version,
                    #   this will no longer exclude empty or all-NA columns
                    #   when determining the result dtypes. To retain the
                    #   old behavior, exclude the relevant entries before
                    #   the concat operation.
                    if self.df_buffer_gap.empty:
                        self.df_buffer_gap = df_buffer_gap_update
                    else:
                        self.df_buffer_gap = concat(
                            [self.df_buffer_gap, df_buffer_gap_update],
                            ignore_index=True,
                        )
                    self.gap_start = None
        # else:
        #     logging.debug(
        #         "Buffer is not consumable yet: size %s vs start_goal %s",
        #         self.buffer_size, self.play_goal_size)
        # logging.debug("Buffer is now filled to %s, while max is %s",
        #               self.buffer_size, self.buffer_size_max)

    def buffer_consume(self, size: int) -> None:
        # logging.debug("Trying to consume %d bytes", size)
        if self.buffer_consumable:
            if self.play_start is None:
                if self.test_start is None:
                    self.test_start = datetime.utcnow()
                self.play_start = datetime.utcnow()

            previous = self.buffer_size
            self.buffer_size -= size
            if self.buffer_size < 0:
                self.buffer_size = 0
                self.gap_start = Timestamp.utcnow()
                self.buffer_consumable = False
                self._add_failure_cause("Video buffer dropped to 0")
                self._set_result(False)
            self.buffer_consumed += previous - self.buffer_size
            # logging.debug("Consumed %d bytes.", previous - self.buffer_size)

    @property
    def size(self) -> int:
        return self.buffer_size

    @property
    def size_max(self) -> int:
        return self.buffer_size_max

    def analyse(self) -> None:
        # Parameters to pass this test:
        #   Packet loss: ?
        if self.gap_start is not None:
            df_buffer_gap_update = DataFrame(
                data={
                    "Start": self.gap_start,
                    "Stop": Timestamp.utcnow(),
                },
                index=RangeIndex(start=0, stop=1),
            )
            # Avoid FutureWarning:
            #   The behavior of DataFrame concatenation with empty
            #   or all-NA entries is deprecated. In a future version,
            #   this will no longer exclude empty or all-NA columns
            #   when determining the result dtypes. To retain the
            #   old behavior, exclude the relevant entries before
            #   the concat operation.
            if self.df_buffer_gap.empty:
                self.df_buffer_gap = df_buffer_gap_update
            else:
                self.df_buffer_gap = concat(
                    [self.df_buffer_gap, df_buffer_gap_update],
                    ignore_index=True,
                )
        if len(self.df_buffer_gap.index) > 0:
            if len(self.df_buffer_gap.index) == 1:
                self._set_log("There is one gap detected.")
            else:
                self._set_log(
                    f"There are {len(self.df_buffer_gap.index)} gaps detected."
                )
        else:
            if self.play_start is None:
                failure_cause = "Never started to play the video."
                self._set_log(failure_cause)
                self._set_result(False)
                self._add_failure_cause(failure_cause)
            else:
                self._set_log("No gaps detected.")
                self._set_result(True)
        # Play start
        if self.play_start is None or self.test_start is None:
            logging.warning(
                "No start analyse: play_start: %s and test_start: %s",
                self.play_start, self.test_start
            )
            return

        initial_wait = self.play_start - self.test_start
        if initial_wait > self.max_initial_wait_time:
            failure_cause = (
                "Initial wait time was larger than"
                f" {self.max_initial_wait_time.total_seconds()} seconds"
                f": {initial_wait.total_seconds()}s"
            )
            self._log = '\n'.join((self._log, failure_cause))
            self._set_result(False)
            self._add_failure_cause(failure_cause)
        else:
            self._log = '\n'.join(
                (
                    self._log, "Initial wait time was smaller than"
                    f" {self.max_initial_wait_time.total_seconds()} seconds"
                    f": {initial_wait.total_seconds()}s"
                )
            )

    def release(self) -> None:
        # NOTE: Nothing to release
        super().release()

    @property
    def log(self) -> str:
        """Return the summary log text.

        .. note::
           Used for unit test report.

        :return: Summary log text.
        :rtype: str
        """
        return self._log

    def render(self) -> str:
        result = "<pre>" + self._log + "</pre>"
        df_state = self.df_buffer[["Buffer state"]]

        df_incoming_bits = to_bitrate((self.df_buffer, 'Buffer incoming'))
        df_outgoing_bits = to_bitrate((self.df_buffer, 'Buffer outgoing'))

        chart = GenericChart(
            "Video buffer timeline",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"},
        )

        chart.add_series(
            list(df_state.itertuples(index=True)), "line", "Buffer state",
            "Datasize", "byte"
        )
        chart.add_series(
            list(df_incoming_bits.itertuples(index=True)),
            "line",
            "Buffer incoming",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_outgoing_bits.itertuples(index=True)),
            "line",
            "Buffer outgoing",
            "Dataspeed",
            "bits/s",
        )
        result += chart.plot(
            f'video_buffer_analyser_container{BufferAnalyser.container_id}'
        )
        BufferAnalyser.container_id += 1
        return result

    def details(self) -> Optional[AnalysisDetails]:
        pass

    def _clear(self) -> None:
        super()._clear()
        self._clear_log()

    def _clear_log(self) -> None:
        self._log = ''

    def _set_log(self, log: str) -> None:
        self._log = log
