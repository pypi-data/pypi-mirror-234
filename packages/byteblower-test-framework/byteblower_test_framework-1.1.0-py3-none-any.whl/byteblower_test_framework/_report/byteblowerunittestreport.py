"""Module for unit test reporting."""
from datetime import datetime  # for type hinting
from typing import Optional  # for type hinting

from pandas import DataFrame  # for type hinting

from .._traffic.flow import Flow  # for type hinting
from .byteblowerreport import ByteBlowerReport
from .unittestreport import UnitTestReport


class ByteBlowerUnitTestReport(ByteBlowerReport):
    """Generate test report in Unit XML format."""

    _FILE_FORMAT: str = 'xml'

    __slots__ = (
        '_title',
        '_unittestreport',
    )

    def __init__(
        self,
        output_dir: Optional[str] = None,
        filename_prefix: str = 'byteblower',
        filename: Optional[str] = None
    ) -> None:
        """Create a ByteBlower Unit test report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.xml``

        where:

        * ``<output_dir>``:  Configurable via ``output_dir``.
          Defaults to the current working directory.
        * ``<prefix>``: Configurable via ``filename_prefix``
        * ``<timestamp>``: Current time. Defined at construction time of the
          ``ByteBlowerReport`` Python object.

        :param output_dir: Override the directory where
           the report file is stored, defaults to ``None``
           (meaning that the "current directory" will be used)
        :type output_dir: str, optional
        :param filename_prefix: Prefix for the ByteBlower report file name,
           defaults to 'byteblower'
        :type filename_prefix: str, optional
        :param filename: Override the complete filename of the report,
           defaults to ``None``
        :type filename: str, optional
        """
        super().__init__(
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            filename=filename
        )
        self._unittestreport = UnitTestReport()

    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        self._unittestreport.set_subtest(flow.name)
        for analyser in flow.analysers:
            failure_causes = analyser.failure_causes
            if failure_causes:
                stderr = '\n'.join(failure_causes)
            else:
                stderr = None
            # NOTE: Set to SKIPPED if no analysis was done:
            if analyser.has_passed is None:
                self._unittestreport.add_skipped(
                    analyser.type,
                    'No analysis performed',
                    stdout=analyser.log,
                    stderr=stderr,
                )
            elif analyser.has_passed:
                self._unittestreport.add_pass(
                    analyser.type,
                    analyser.log,
                    stderr=stderr,
                )
            else:
                fail_message = stderr or 'see analysis log for details'
                self._unittestreport.add_fail(
                    analyser.type,
                    fail_message,
                    stdout=analyser.log,
                )

    def render(
        self, api_version: str, framework_version: str, port_list: DataFrame,
        scenario_start_timestamp: Optional[datetime],
        scenario_end_timestamp: Optional[datetime]
    ) -> None:
        """Render the report.

        :param port_list: Configuration of the ByteBlower Ports.
        :type port_list: DataFrame
        """
        self._unittestreport.save(name=self.report_url)

    def clear(self) -> None:
        """Start with empty report contents."""
        self._unittestreport = UnitTestReport()
