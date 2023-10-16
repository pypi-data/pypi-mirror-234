"""Containing the data gathering interface definition."""
from abc import ABC, abstractmethod


class DataGatherer(ABC):
    """Data gathering interface definition."""

    __slots__ = ()

    def __init__(self) -> None:
        """Make a new data gatherer."""

    def prepare(self) -> None:
        """
        Prepare the receivers to process expected data.

        .. note::
           Virtual method.
        """

    def process(self) -> None:
        """
        .. note::
           Virtual method.
        """

    def updatestats(self) -> None:
        """
        .. note::
           Virtual method.
        """

    def summarize(self) -> None:
        """
        Store the final results.

        This can contain totals, summary, ...

        .. note::
           Virtual method.
        """

    @abstractmethod
    def release(self) -> None:
        """Release all resources used on the ByteBlower system."""
