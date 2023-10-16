"""Module for reporting in HTML format."""
import logging
from datetime import datetime  # for type hinting
from os.path import abspath, dirname, join
from typing import Iterable, List, Optional, Sequence  # for type hinting

from highcharts_excentis import Highchart
from jinja2 import Environment, FileSystemLoader
from pandas import DataFrame  # for type hinting

from .._analysis.analyseraggregator import HtmlAnalyserAggregator
from .._analysis.latencyaggregator import HtmlLatencyAggregator
from .._traffic.flow import Flow  # for type hinting
from .byteblowerreport import ByteBlowerReport
from .helper import snake_to_title
from .options import Layer2Speed

_PACKAGE_DIRECTORY = dirname(abspath(__file__))

_FLOW_CONFIG_ROW_TMPL = \
    '<tr><th>{name}</th> <td>{value!s}</td></tr>'
_FLOW_PORT_INFO_TMPL = '{name} ({ip!s})'

_QUOTES = [
    (
        "The greatest glory in living lies not in never falling," +
        "<br>but in rising every time we fall.",
        "Byteblower rises with you, optimizing networks" +
        "<br>to new heights of success.",
    ),
    (
        "In the journey of a thousand miles," +
        "<br>the first step is the most important.",
        "Begin your network optimization journey" +
        " with Byteblower, your trusted guide.",
    ),
    (
        "Success is not final, failure is not fatal:" +
        "<br>It is the courage to continue that counts.",
        "Byteblower empowers you to persevere" +
        "<br>in the pursuit of network perfection.",
    ),
    (
        "Believe you can and you're halfway there.",
        "Byteblower believes in your network's potential," +
        " working tirelessly to ensure it reaches its destination.",
    ),
    (
        "The only limit to our realization of tomorrow" +
        "<br>will be our doubts of today.",
        "With Byteblower by your side, doubtlessly" +
        "<br>forge ahead to unlock network excellence.",
    ),
    (
        "Embrace the challenges that come your way," +
        "<br>for they are the stepping stones" + "<br>to greatness.",
        "Byteblower, your faithful companion in the world of testing, is here"
        + "<br>to help you conquer those challenges," +
        " one network improvement at a time",
    ),
]


class ByteBlowerHtmlReport(ByteBlowerReport):
    """Generate a report in HTML format.

    Generates summary information of test status,
    test configuration and results from all flows.

    This report contains:

    * A global PASS/FAIL result
    * Port configuration table
    * Correlated results

       * Aggregated results over all flows
         (supporting aggregation of *over time* graphs and *summary* table)
    * Per-flow results

       * Flow configuration
       * Results for all Analysers attached to the flow
    """

    _FILE_FORMAT: str = 'html'

    __slots__ = (
        '_title',
        '_test_passed',
        '_layer2_speed',
        '_env',
        '_template',
        '_test_section_template',
        '_flow_section_template',
        '_flows',
        '_analyseraggregator',
        '_latencyaggregator',
    )

    def __init__(
        self,
        output_dir: Optional[str] = None,
        filename_prefix: str = 'byteblower',
        filename: Optional[str] = None,
        layer2_speed: Optional[Layer2Speed] = Layer2Speed.frame
    ) -> None:
        """Create a ByteBlower HTML report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.html``

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
        :param layer2_speed: Configuration setting to select the layer 2
           speed reporting, defaults to :attr:`~.options.Layer2Speed.frame`
        :type layer2_speed: ~options.Layer2Speed, optional
        """
        super().__init__(
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            filename=filename
        )
        self._layer2_speed = layer2_speed
        self._title: str = 'ByteBlower report'
        self._test_passed: Optional[bool] = None
        # Configure Jinja and ready the template
        self._env = Environment(
            loader=FileSystemLoader(
                searchpath=join(_PACKAGE_DIRECTORY, 'templates')
            )
        )
        self._template = self._env.get_template('report.html')
        self._test_section_template = self._env.get_template(
            'test_section.html'
        )
        self._flow_section_template = self._env.get_template(
            'flow_section.html'
        )
        self._flows: List[str] = list()
        self._analyseraggregator = HtmlAnalyserAggregator()
        self._latencyaggregator = HtmlLatencyAggregator()

    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        self._render_flow(flow)

        for analyser in flow.analysers:
            # NOTE: The sorted_analysers list may not contain *all* analysers,
            # So we must make sure that we check them all.
            if self._test_passed is None:
                self._test_passed = analyser.has_passed
            elif analyser.has_passed is not None:
                self._test_passed = self._test_passed and analyser.has_passed

            self._latencyaggregator.add_analyser(analyser)

        sorted_analysers = self._analyseraggregator.order_by_support_level(
            flow.analysers
        )
        for analyser in sorted_analysers:
            logging.debug(
                'Aggregating supported analyser %s',
                type(analyser).__name__
            )
            self._analyseraggregator.add_analyser(analyser)

            # NOTE - Avoid aggregating twice with the same Flow data
            break

    def render(
        self, api_version: str, framework_version: str, port_list: DataFrame,
        scenario_start_timestamp: Optional[datetime],
        scenario_end_timestamp: Optional[datetime]
    ) -> None:
        """Render the report.

        :param port_list: Configuration of the ByteBlower Ports.
        :type port_list: DataFrame
        """
        correlation_html = '\n'.join(self._render_aggregators())
        quote_head, quote_tagline = _QUOTES[-1]

        chart = Highchart(offline=True)
        chart.buildhtmlheader()
        js_resources = chart.htmlheader

        with open(self.report_url, 'w', encoding='utf-8') as report_file:
            report_file.write(
                self._template.render(
                    title=self._title,
                    test_passed=self._test_passed,
                    api_version=api_version,
                    framework_version=framework_version,
                    scenario_start_timestamp=scenario_start_timestamp,
                    scenario_end_timestamp=scenario_end_timestamp,
                    js_resources=js_resources,
                    ports=port_list.to_html(),
                    correlated=correlation_html,
                    flows=self._flows,
                    quote_head=quote_head,
                    quote_tagline=quote_tagline
                )
            )

    def clear(self) -> None:
        """Start with empty report contents."""
        self._flows = []
        self._analyseraggregator = HtmlAnalyserAggregator()
        self._latencyaggregator = HtmlLatencyAggregator()

    # def _render_flow(self, name, type, source, destination, config, tests):
    def _render_flow(self, flow: Flow) -> None:
        tests = ''
        for analyser in flow.analysers:
            tests += self._render_test(
                analyser.type,
                analyser.has_passed,
                analyser.failure_causes,
                analyser.render(),
            )
        config = ""
        for k in flow._CONFIG_ELEMENTS:
            if k in ('analysers', 'source', 'destination', 'name', 'type'):
                continue
            config += _FLOW_CONFIG_ROW_TMPL.format(
                name=snake_to_title(k), value=getattr(flow, k)
            )

        source = _FLOW_PORT_INFO_TMPL.format(
            name=flow.source.name, ip=flow.source.ip
        )
        destination = _FLOW_PORT_INFO_TMPL.format(
            name=flow.destination.name, ip=flow.destination.ip
        )
        self._flows.append(
            self._flow_section_template.render(
                name=flow.name,
                type=flow.type,
                source=source,
                destination=destination,
                config=config,
                runtime_errors=flow.runtime_error_info,
                tests=tests,
            )
        )

    def _render_test(
        self, test: str, has_passed: Optional[bool],
        failure_causes: Sequence[str], log: str
    ) -> str:
        """Render the log from the test scenario."""
        if has_passed is None:
            pass_or_fail = (
                '<font size="3" color="orange">No analysis performed</font>'
            )
        elif has_passed:
            pass_or_fail = '<font size="3" color="green">PASS</font>'
        else:
            pass_or_fail = '<font size="3" color="red">FAIL</font>'

        return self._test_section_template.render(
            test=test,
            passorfail=pass_or_fail,
            failure_causes=failure_causes,
            log=log,
        )

    def _render_aggregators(self) -> Iterable[str]:
        # Render the aggregators where we can do aggregation
        if self._latencyaggregator.can_render():
            yield self._latencyaggregator.render()
        if self._analyseraggregator.can_render():
            yield self._analyseraggregator.render(self._layer2_speed)
