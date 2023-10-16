import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import (  # for type hinting
    TYPE_CHECKING,
    Any,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)

from .._endpoint.ipv4.nat import NattedPort  # for type hinting
from .._endpoint.port import Port  # for type hinting

if TYPE_CHECKING:
    # NOTE: Import does not work at runtime: cyclic import dependencies
    # See also: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#import-cycles, pylint: disable=line-too-long
    from .._analysis.flow_analyser import FlowAnalyser  # for type hinting
    # NOTE: Used for type hinting only
    from .._helpers.syncexec import SynchronizedExecutable

# Type aliases
# TODO - Make the RuntimeErrorInfo a real (base) object ?
#: Flow-specific information about runtime errors
RuntimeErrorInfo = Mapping[str, Any]


class Flow(ABC):
    """Base class of a flow between one and one or more ByteBlower ports."""

    __slots__ = (
        '_source',
        '_destination',
        '_name',
        '_tags',
        '_analysers',
    )

    _number = 1

    _CONFIG_ELEMENTS = (
        'source',
        'destination',
        'name',
        'analysers',
        'type',
    )

    def __init__(
        self,
        source: Union[Port, NattedPort],
        destination: Union[Port, NattedPort],
        # *args,
        name: Optional[str] = None,
        **kwargs
    ) -> None:

        self._source = source
        self._destination = destination

        if name is not None:
            self._name = name
        else:
            self._name = 'Flow ' + str(Flow._number)

        if kwargs:
            logging.error(
                'Unsupported keyword arguments for Flow %r: %r', self._name, [
                    '{}={!r}'.format(key, value)
                    for key, value in kwargs.items()
                ]
            )
            raise ValueError(
                'Unsupported configuration parameters'
                f' for Flow {self._name!r}: {[key for key in kwargs]!r}'
            )

        if self._source.failed:
            raise ValueError(
                'Cannot send from ByteBlower Port {!r} because address'
                ' configuration failed.'.format(self._source.name)
            )

        if self._destination.failed:
            raise ValueError(
                'Cannot send to ByteBlower Port {!r} because address'
                ' configuration failed.'.format(self._destination.name)
            )

        if self._source.is_natted and self._destination.is_natted:
            raise ValueError(
                'Cannot send between two ByteBlower Ports ({!r} <> {!r})'
                ' behind a NAT.'.format(
                    self._source.name, self._destination.name
                )
            )

        self._analysers: List['FlowAnalyser'] = []

        self._tags: List[str] = list()
        self.add_tag('from_' + self._source.name)
        for tag in self._source.tags:
            self.add_tag('from_' + tag)
        self.add_tag('to_' + self._destination.name)
        for tag in self._destination.tags:
            self.add_tag('to_' + tag)

        Flow._number += 1

    @property
    def source(self) -> Union[Port, NattedPort]:
        return self._source

    @property
    def destination(self) -> Union[Port, NattedPort]:
        return self._destination

    @property
    def name(self) -> str:
        return self._name

    @property
    @abstractmethod
    def initial_time_to_wait(self) -> timedelta:
        """Return the time to wait before the flow starts."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def duration(self) -> timedelta:
        """Returns the duration of the flow.

        :raises NotDurationBased: If the Flow is sized based.
        :raises InfiniteDuration: If the flow duration is not set.
        :return: duration of the flow.
        :rtype: timedelta
        """
        raise NotImplementedError()

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def analysers(self) -> Sequence['FlowAnalyser']:
        """Return the list of flow analysers added to this Flow.

        :return: List of added flow analysers
        :rtype: Sequence[FlowAnalyser]
        """
        return self._analysers

    @property
    def config(self) -> Sequence[str]:
        configs = []

        for k in self._CONFIG_ELEMENTS:
            if k == 'analysers':
                continue

            if k == 'source' or k == 'destination':
                port: Port = getattr(self, k)
                v = port.ip
            else:
                v = getattr(self, k)
            configs.append("{k!s} = {v!s}".format(k=k, v=v))
        return configs

    @property
    @abstractmethod
    def finished(self) -> bool:
        """Returns True if the flow is done."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def runtime_error_info(self) -> RuntimeErrorInfo:
        """Returns implementation-specific runtime error info."""
        raise NotImplementedError()

    def add_analyser(self, analyser: 'FlowAnalyser') -> None:
        analyser._add_to_flow(self)
        self._analysers.append(analyser)

    def apply(self, **kwargs) -> Iterable['SynchronizedExecutable']:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.apply()
        # NOTE: turn this function into an "empty" generator
        #
        # See also
        #   https://stackoverflow.com/questions/13243766/how-to-define-an-empty-generator-function/61496399#61496399  # pylint: disable=line-too-long
        # for considerations regarding performance.
        yield from ()

    def process(self) -> None:
        for analyser in self._analysers:
            analyser.process()

    def updatestats(self) -> None:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.updatestats()

    def wait_until_finished(self, wait_for_finish: timedelta) -> None:
        """
        .. note::
           Virtual method.
        """

    def stop(self) -> None:
        """
        Stop all traffic generation and analysis for this flow.

        .. note::
            Virtual hook method for child implementations.

        .. versionadded:: 1.1.0
        """

    def analyse(self) -> None:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.analyse()

    @abstractmethod
    def release(self) -> None:
        """
        Release all resources used on the ByteBlower system.

        Releases all resources related to traffic generation and analysis.

        .. note::
           The resources related to endpoints and server themselves
           are not released.
        """
        for analyser in self._analysers:
            analyser.release()

    def add_tag(self, new_tag) -> None:
        new_tag = new_tag.lower()
        if new_tag not in self._tags:
            self._tags.append(new_tag)
