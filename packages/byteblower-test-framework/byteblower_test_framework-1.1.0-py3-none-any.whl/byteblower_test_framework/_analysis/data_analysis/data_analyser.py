"""Contains the data analyser interface definition."""
from typing import List, Optional, Sequence  # for type hinting


class DataAnalyser(object):
    """Data analyser interface definition."""

    __slots__ = (
        '_result',
        '_failure_causes',
        '_log',
    )

    def __init__(self) -> None:
        """Make a new data analyser."""
        self._result: Optional[bool] = None
        self._failure_causes: List[str] = []
        self._log: str = ''

    def prepare(self) -> None:
        """Prepare the analyser for starting the test.

        .. note::
           Virtual method.
        """
        self._clear()

    def analyse(self) -> None:
        """
        Analyse the gathered data.

        .. note::
           Virtual method.
        """
        pass

    @property
    def has_passed(self) -> Optional[bool]:
        """
        Return whether the test passed or not.

        Returns None if no data analysis was done.
        """
        return self._result

    @property
    def failure_causes(self) -> Sequence[str]:
        """Return failures which caused the analyser to fail the test."""
        return self._failure_causes

    @property
    def log(self) -> str:
        """Return the analysis summary log."""
        return self._log

    def _clear(self) -> None:
        self._clear_result()
        self._clear_failure_causes()
        self._clear_log()

    def _clear_result(self) -> None:
        self._result = None

    def _set_result(self, result: bool) -> None:
        self._result = result

    def _clear_failure_causes(self) -> None:
        self._failure_causes.clear()

    def _add_failure_cause(self, failure_cause: str) -> None:
        assert (
            failure_cause is not None
        ), "Internal error: Data Analyser failure cause is None"
        self._failure_causes.append(failure_cause)

    def _clear_log(self) -> None:
        self._log = ''

    def _set_log(self, log: str) -> None:
        self._log = log
