"""Contains the data analysis renderer interface."""
from typing import Any, Mapping, Optional

# Type aliases
AnalysisDetails = Mapping[str, Any]


class Renderer(object):
    """Renderer interface of Data analysis."""

    __slots__ = ()
    container_id = 0

    def __init__(self) -> None:
        """Make a new reporter."""
        pass

    def render(self) -> str:
        """
        Return the detailed analysis results in HTML format.

        .. note::
           Virtual method.
        """
        pass

    def details(self) -> Optional[AnalysisDetails]:
        """
        Return the detailed analysis results in pandas-compatible objects.

        Can be ``None`` if no detailed results are available or applicable.

        .. note::
           Virtual method.
        """
        pass

    def _verbatim(self, text: str) -> str:
        return '<pre>' + text + '</pre>'
