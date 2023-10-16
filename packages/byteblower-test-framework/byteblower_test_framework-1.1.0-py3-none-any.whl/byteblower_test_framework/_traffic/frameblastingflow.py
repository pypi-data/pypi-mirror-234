from datetime import timedelta  # for type hinting
from statistics import mean
from typing import (  # for type hinting
    TYPE_CHECKING,
    Iterable,
    List,
    Optional,
    Sequence,
    Union,
)

from byteblowerll.byteblower import Stream as TxStream  # for type hinting
from byteblowerll.byteblower import StreamRuntimeStatus  # for type hinting
from byteblowerll.byteblower import TransmitStatus

from .._analysis.data_gathering.stream import \
    StreamDataGatherer  # for type hinting
from .._analysis.data_gathering.stream import StreamFrameCountDataGatherer
from .._analysis.storage.frame_count import FrameCountData
from .._analysis.storage.stream import StreamStatusData
from .._endpoint.ipv4.nat import NattedPort  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .._helpers.syncexec import SynchronizedExecutable
from .._traffic.stream import StreamErrorStatus
from ..exceptions import InfiniteDuration
from .flow import RuntimeErrorInfo  # for type hinting
from .flow import Flow
from .frame import Frame  # for type hinting
from .imix import Imix  # for type hinting

if TYPE_CHECKING:
    # NOTE: Used in documentation
    from .._analysis.flow_analyser import FlowAnalyser

DEFAULT_FRAME_RATE: float = 100.0
INFINITE_NUMBER_OF_FRAMES: int = -1
DEFAULT_NUMBER_OF_FRAMES: int = INFINITE_NUMBER_OF_FRAMES


class FrameBlastingFlow(Flow):

    __slots__ = (
        '_stream',
        '_stream_status_data',
        '_stream_frame_count_data',
        '_stream_data_gatherer',
        '_frame_rate',
        '_number_of_frames',
        '_initial_time_to_wait',
        '_imix',
        '_frame_list',
    )

    _CONFIG_ELEMENTS = Flow._CONFIG_ELEMENTS + (
        'frame_rate',
        'number_of_frames',
        'initial_time_to_wait',
    )

    _stream_data_gatherer_class = StreamFrameCountDataGatherer

    def __init__(
        self,
        source: Union[Port, NattedPort],
        destination: Union[Port, NattedPort],
        name: Optional[str] = None,
        bitrate: Optional[float] = None,  # [bps]
        frame_rate: Optional[float] = None,  # [fps]
        number_of_frames: Optional[int] = None,
        duration: Optional[Union[timedelta, float, int]] = None,  # [seconds]
        initial_time_to_wait: Optional[Union[timedelta, float,
                                             int]] = None,  # [seconds]
        frame_list: Optional[Sequence[Frame]] = None,
        imix: Optional[Imix] = None,
        **kwargs
    ) -> None:
        """Create a Frame Blasting flow.

        :param source: Sending port of the voice stream
        :type source: Union[Port, NattedPort]
        :param destination: Receiving port of the voice stream
        :type destination: Union[Port, NattedPort]
        :param name: Name of this Flow, defaults to auto-generated name
           when set to ``None``.
        :type name: str, optional
        :param frame_rate: Rate at which the frames are transmitted
           (in frames per second), mutual exclusive with ``bitrate``,
           defaults to :const:`DEFAULT_FRAME_RATE` when ``bitrate``
           is not provided.
        :type frame_rate: float, optional
        :param bitrate: Rate at which the bits are transmitted
           (in bit per second). Excludes the VLAN tag bytes
           (*when applicable*), mutual exclusive with ``frame_rate``,
           defaults to None.
        :type bitrate: float, optional
        :raises ValueError: When both ``frame_rate`` and ``bitrate`` are
           given.
        :param number_of_frames: Number of frames to transmit,
           defaults to :const:`DEFAULT_NUMBER_OF_FRAMES`
        :type number_of_frames: int, optional
        :param duration: Duration of the flow in seconds,
           defaults to None (use number_of_frames instead)
        :type duration: Union[timedelta, float, int], optional
        :param initial_time_to_wait: Initial time to wait to start the flow.
           In seconds, defaults to None (start immediately)
        :type initial_time_to_wait: Union[timedelta, float, int], optional
        :param frame_list: List of frames to transmit,
           mutual exclusive with ``imix``, defaults to None
        :type frame_list: Sequence[Frame], optional
        :param imix: Imix definition of frames to transmit,
           mutual exclusive with ``frame_list``, defaults to None
        :type imix: Imix, optional
        :raises ValueError: When both ``imix`` and ``frame_list`` are given
           or when none of both is given.
        """
        super().__init__(source, destination, name=name, **kwargs)

        self._frame_rate = frame_rate

        self._imix = imix

        if self._imix and frame_list:
            raise ValueError(
                f'Flow {self._name!r}: Please provide'
                ' either IMIX or frame list but not both.'
            )
        if self._imix:
            frame_list = self._imix._generate(self._source)

        # Calculate average frame size
        frame_sizes = (frame.length for frame in frame_list)
        avg_frame_size = mean(frame_sizes)  # [Bytes]

        if bitrate and frame_rate:
            raise ValueError(
                f'Flow {self._name!r}: Please provide'
                ' either bitrate or frame rate but not both.'
            )

        # Convert bitrate to frame rate
        if bitrate:
            self._frame_rate = (bitrate / 8) / avg_frame_size

        if not self._frame_rate:
            self._frame_rate = DEFAULT_FRAME_RATE

        if duration is not None:
            if isinstance(duration, timedelta):
                # Convert to float
                duration = duration.total_seconds()
            # else:
            #     # Already float/int:
            #     duration = duration or 0
            self._number_of_frames = int(duration * self._frame_rate)
        elif number_of_frames is not None:
            self._number_of_frames = number_of_frames
        else:
            self._number_of_frames = DEFAULT_NUMBER_OF_FRAMES

        if isinstance(initial_time_to_wait, (float, int)):
            # Convert to timedelta
            self._initial_time_to_wait = timedelta(
                seconds=initial_time_to_wait
            )
        else:
            # Either already timedelta or None:
            # Default to 0s
            self._initial_time_to_wait = initial_time_to_wait or timedelta()

        # Create the stream
        self._stream: TxStream = self._source.bb_port.TxStreamAdd()
        self._stream.InitialTimeToWaitSet(
            int(self._initial_time_to_wait.total_seconds() * 1e9)
        )
        self._stream_status_data: Optional[StreamStatusData] = None
        self._stream_frame_count_data: Optional[FrameCountData] = None
        self._stream_data_gatherer: Optional[StreamDataGatherer] = None

        self._frame_list: List[Frame] = []
        for frame in frame_list:
            frame._add(self._source, self._destination, self._stream)
            self._frame_list.append(frame)

    def initialize_stream_data_gatherer(self) -> None:
        """
        Make sure that the stream data gatherer is available for testing.

        Should be called by the :class:`FlowAnalyser` or the user *before*
        starting a test when he needs ByteBlower stream (packet count) data.
        """
        if self._stream_data_gatherer is None:
            self._stream_status_data = StreamStatusData()
            self._stream_frame_count_data = FrameCountData()
            self._stream_data_gatherer = self._stream_data_gatherer_class(
                self._stream_status_data, self._stream_frame_count_data, self
            )

    @property
    def stream_frame_count_data(self) -> Optional[FrameCountData]:
        """Get the frame count data from the stream analysis.

        .. note::
           Initially created by calling
           :meth:`initialize_stream_data_gatherer()`

        :return: Frame count data
        :rtype: FrameCountData
        """
        return self._stream_frame_count_data

    @property
    def frame_rate(self) -> float:
        return self._frame_rate

    @property
    def frame_list(self) -> Sequence[Frame]:
        return self._frame_list

    @property
    def number_of_frames(self) -> int:
        return self._number_of_frames

    @property
    def duration(self) -> timedelta:
        """Returns the duration of the FrameBlasting flow.

        :raises InfiniteDuration: If the flow duration is configured
           to run forever.
        :return: duration of the flow.
        :rtype: timedelta
        """
        if self._number_of_frames == INFINITE_NUMBER_OF_FRAMES:
            raise InfiniteDuration()
        duration = self._number_of_frames / self._frame_rate
        return timedelta(seconds=duration)

    @property
    def initial_time_to_wait(self) -> timedelta:
        """Return the time to wait before the flow starts."""
        return self._initial_time_to_wait

    @property
    def finished(self) -> bool:
        """Returns True if the flow is done."""
        stream_status: StreamRuntimeStatus = self._stream.StatusGet()
        stream_status.Refresh()
        transmit_status = stream_status.StatusGet()
        return transmit_status == TransmitStatus.INACTIVE

    @property
    def runtime_error_info(self) -> RuntimeErrorInfo:
        if self._stream_status_data is not None:
            error_status = self._stream_status_data.error_status
            if error_status != StreamErrorStatus.NONE:
                error_source = self._stream_status_data.error_source
                return {
                    'status': error_status,
                    'source': error_source,
                }
        return {}

    # def add_frame(self, frame: Frame) -> None:
    #     frame._add(self._source, self._destination, self._stream)
    #     self._frame_list.append(frame)

    def apply(self,
              maximum_run_time: Optional[timedelta] = None,
              **kwargs) -> Iterable[SynchronizedExecutable]:
        # if initial_time_to_wait is set, subtract this wait time
        # from the scenario duration

        duration: timedelta = maximum_run_time - self.initial_time_to_wait
        number_of_frames = int(duration.total_seconds() * self._frame_rate)
        if (self._number_of_frames == INFINITE_NUMBER_OF_FRAMES
                or number_of_frames < self._number_of_frames):
            self._number_of_frames = number_of_frames

        self._stream.InterFrameGapSet(int(1000000000 / self._frame_rate))
        self._stream.NumberOfFramesSet(self._number_of_frames)

        if self._stream_data_gatherer is not None:
            self._stream_data_gatherer.prepare()

        yield from super().apply(**kwargs)
        yield SynchronizedExecutable(self._stream)

    def process(self) -> None:
        if self._stream_data_gatherer is not None:
            self._stream_data_gatherer.process()
        super().process()

    def updatestats(self) -> None:
        if self._stream_data_gatherer is not None:
            self._stream_data_gatherer.updatestats()
        super().updatestats()

    def stop(self) -> None:
        self._stream.Stop()
        super().stop()

    def analyse(self) -> None:
        if self._stream_data_gatherer is not None:
            self._stream_data_gatherer.summarize()
        super().analyse()

    def release(self) -> None:
        super().release()
        if self._stream_data_gatherer is not None:
            self._stream_data_gatherer.release()
        for frame in self._frame_list:
            frame.release(self._stream)
        self._source.bb_port.TxStreamRemove(self._stream)
        del self._stream
