"""ByteBlower Test Scenario interface module."""
import logging
from datetime import datetime, timedelta
from time import sleep
from typing import List, Optional, Sequence, Union  # for type hinting

from byteblowerll.byteblower import ScheduleGroup  # for type hinting
from byteblowerll.byteblower import ByteBlower
from pandas import DataFrame

from ._endpoint.ipv4.nat import NattedPort  # for type hinting
from ._endpoint.port import Port  # for type hinting
from ._helpers.syncexec import SynchronizedExecution, synchronized_start
from ._host.server import Server  # for type hinting
from ._report.byteblowerreport import ByteBlowerReport  # for type hinting
from ._traffic.flow import Flow  # for type hinting
from ._version import version
from .exceptions import InfiniteDuration, NotDurationBased

#: Default time to wait for sessions closing and final packets
#: being received, defaults to timedelta(seconds=5)
DEFAULT_WAIT_FOR_FINISH: timedelta = timedelta(seconds=5)
DEFAULT_SCENARIO_DURATION: timedelta = timedelta(seconds=10)


class Scenario(object):
    """ByteBlower Test Scenario interface."""

    __slots__ = (
        '_flows',
        '_servers',
        '_bb_reports',
        '_schedule_group',
        '_start_timestamp',
        '_end_timestamp',
    )

    def __init__(self) -> None:
        """Make a base test scenario."""
        self._flows: List[Flow] = []
        self._servers: List[Server] = []
        self._bb_reports: List[ByteBlowerReport] = []
        self._schedule_group: ScheduleGroup
        self._start_timestamp: Optional[datetime] = None
        self._end_timestamp: Optional[datetime] = None

    def __del__(self) -> None:
        """Cleanup of test scenario."""

    def add_report(self, report: ByteBlowerReport) -> None:
        self._bb_reports.append(report)

    def add_flow(self, flow: Flow) -> None:
        if flow.source.failed or flow.destination.failed:
            logging.debug(
                'Flow %r is not added to the scenario because either'
                ' source or destination address configuration failed.',
                flow.name
            )
            return
        self._flows.append(flow)
        # Check if we know the server. If not, add it.

        for server in (flow.source.server, flow.destination.server):
            if server in self._servers:
                # We have nothing to do
                logging.debug('Test:Server already in list')
            else:
                logging.debug('Test:Adding new server.')
                self._servers.append(server)

    def run(
        self,
        maximum_run_time: Optional[timedelta] = None,
        wait_for_finish: Optional[timedelta] = None,
        duration: Optional[timedelta] = None,
    ) -> None:
        """Run the scenario.

        * if ``max_run_time`` is specified, the scenario will limit the run
          time (*initial time to wait* + *duration*) of all flows. The scenario
          will stop after the ``max_run_time`` has passed. Also flow which
          are not duration-based will be stopped.
        * If the ``max_run_time`` is not specified it will run for the
          the time of the flow with the longest run time (*initial time to
          wait* + *duration*). The scenario will wait (*indefinitely*) for
          any non duration-based flow to finish.

        The ``duration`` parameter is kept for backward compatibility with
        older (*beta*) versions of the ByteBlower Test Framework. It will be
        removed definitely with the final version 1.0 release.

        :param maximum_run_time: maximum run time of the scenario,
           defaults to None
        :type maximum_run_time: Optional[timedelta], optional
        :param wait_for_finish: Time to wait for sessions closing and final
           packets being received, defaults to timedelta(seconds=5)
        :type wait_for_finish: timedelta, optional
        :param duration: Backward-compatible parameter for the
           ``max_run_time``, defaults to None
        :type duration: Optional[timedelta], optional
        """
        if duration is not None:
            if maximum_run_time is None:
                maximum_run_time = duration
                logging.warning(
                    "DEPRECATED: Scenario.run(): 'duration' is replaced by"
                    " 'maximum_run_time'. This parameter will be removed in"
                    " the final v1.0.0 release."
                )
            else:
                logging.warning(
                    "DEPRECATED: Scenario.run(): 'duration' is replaced by"
                    " 'maximum_run_time'. 'maximum_run_time' is also given"
                    " and preferred."
                )
        if wait_for_finish is None:
            wait_for_finish = DEFAULT_WAIT_FOR_FINISH
        self._start(maximum_run_time)
        self._wait_until_finished(maximum_run_time, wait_for_finish)
        self._stop()
        self._analyse()
        logging.info('Test is done')

    def release(self) -> None:
        """
        Release all resources used on the ByteBlower system.

        Releases all resources related to traffic generation and analysis.

        .. note::
           The ByteBlower Ports / Endpoints themselves are not released.
        """
        # FIXME: This is not possible (yet):
        # bb_root: ByteBlower = ByteBlower.InstanceGet()
        # bb_root.ScheduleGroupDestroy(self._schedule_group)
        del self._schedule_group

        for flow in self._flows:
            flow.release()

    def _start(self, maximum_run_time: Optional[timedelta]) -> None:
        # TODO: Setting the *start timestamp* here is not 100% consistent
        #       with the GUI.
        # The GUI uses start/end as indication when you *can* see data traffic
        # on the network under test. Here, the endpoints are already
        # initialized and the flows already prepared and configured.
        self._start_timestamp = datetime.utcnow()

        # If scenario maximum_run_time is specified
        # It will limit the run time of *all* flows
        if maximum_run_time is None:
            # use the longest flow run time
            maximum_run_time = max(
                (self._get_flow_run_time(flow) for flow in self._flows)
            )
            # in case no durations were configured
            if maximum_run_time == timedelta():
                maximum_run_time = DEFAULT_SCENARIO_DURATION

        # Prepare the flows for traffic generation / analysis
        sync_exec = SynchronizedExecution()
        for flow in self._flows:
            flow_startable = flow.apply(maximum_run_time=maximum_run_time)
            sync_exec.add(flow_startable)

        # Start the involved schedulable objects synchronized
        bb_root: ByteBlower = ByteBlower.InstanceGet()
        schedule_group: ScheduleGroup = bb_root.ScheduleGroupCreate()
        self._schedule_group = schedule_group
        sync_exec.execute(synchronized_start(schedule_group))

    def _wait_until_finished(
        self, maximum_run_time: Optional[timedelta], wait_for_finish: timedelta
    ) -> None:
        previous = datetime.now()
        start_time = previous
        iteration = 0

        while True:
            # sleep 1 millisecond
            sleep(0.001)
            all_flows_finished = True
            do_updatestats = (datetime.now() - previous) > timedelta(seconds=1)
            if do_updatestats:
                logging.debug('Update stats, iteration is %u', iteration)
            for flow in self._flows:
                if do_updatestats:
                    flow.updatestats()
                else:
                    flow.process()

                all_flows_finished = all_flows_finished and flow.finished

            if do_updatestats:
                iteration += 1
                previous = datetime.now()

            scenario_duration_finished = maximum_run_time is not None and (
                previous - start_time
            ) >= maximum_run_time
            if scenario_duration_finished or (maximum_run_time is None
                                              and all_flows_finished):
                # Scenario finished
                break

        # Wait for TCP to finish if flow uses TCP
        finish_time = datetime.now() + wait_for_finish
        for flow in self._flows:
            remaining_wait_time = finish_time - datetime.now()
            if remaining_wait_time > timedelta(seconds=0):
                flow.wait_until_finished(remaining_wait_time)

            if datetime.now() >= finish_time:
                break

    def _stop(self) -> None:
        # 1. Cancel all schedules:
        self._schedule_group.Stop()

        # # 2. Stop all traffic / analysis
        for flow in self._flows:
            flow.stop()

        sleep(1)

    def _analyse(self) -> None:
        for flow in self._flows:
            flow.analyse()
        # TODO: Setting the *stop timestamp* here is not 100% consistent
        #       with the GUI.
        # The GUI uses start/end as indication when you *can* see data traffic
        # on the network under test. Here, the endpoints and flows are still
        # configured. So, they might send out packets on the network.
        self._end_timestamp = datetime.utcnow()

    @property
    def flows(self) -> Sequence[Flow]:
        """Returns the list of flows added to this Scenario.

        :return: List of added flows.
        :rtype: List[Flow]
        """
        return self._flows

    @property
    def start_timestamp(self) -> Optional[datetime]:
        """Return the timestamp when the Scenario was started.

        The start timestamp is the timestamp right before starting the flows.
        This is logged at the start of the :meth:`Scenario.run` call.

        .. note::
           The time between endpoint and flow initialization is not taken into
           account here.

        :return: Start timestamp of the last run
        :rtype: Optional[datetime]
        """
        return self._start_timestamp

    @property
    def end_timestamp(self) -> Optional[datetime]:
        """Return the timestamp when the Scenario was finished.

        The end timestamp is the timestamp right after
        stopping the flows and analysing the final results.
        This is logged at the end of the :meth:`Scenario.run` call.

        .. note::
           The time between flow analysis and flow and endpoint cleanup
           is not taken into account here.

        :return: End time of the last run
        :rtype: Optional[datetime]
        """
        return self._end_timestamp

    @property
    def duration(self) -> Optional[datetime]:
        """Return the actual duration of the last Scenario run.

        The duration is calculated as
        :meth:`start_timestamp` - :meth:`end_timestamp`.

        :return: Actual duration of the last run.
        :rtype: Optional[datetime]
        """
        if (self._start_timestamp is not None
                and self._end_timestamp is not None):
            return self._end_timestamp - self._start_timestamp
        return None

    def _port_list(self) -> DataFrame:
        ports: List[Union[Port, NattedPort]] = []
        for flow in self._flows:
            if flow.source not in ports:
                ports.append(flow.source)
            if flow.destination not in ports:
                ports.append(flow.destination)

        df = DataFrame(
            columns=[
                'IP address',
                'Gateway',
                'Network',
                'VLAN (PCP / DEI)',
                'Public IP',
            ],
            index=[port.name for port in ports],
        )
        for port in ports:
            if port.is_natted:
                public_ip = port.public_ip
            else:
                public_ip = '-'
            vlan_configs = port.vlan_config
            if vlan_configs:
                vlan_info = 'Outer ' + ' > '.join(
                    (
                        f'{vlan_id} ({vlan_pcp} / {vlan_dei})' for _vlan_tpid,
                        vlan_id, vlan_dei, vlan_pcp in vlan_configs
                    )
                )
            else:
                vlan_info = 'No'
            df.loc[port.name] = [
                port.ip,
                port.gateway,
                port.network,
                vlan_info,
                public_ip,
            ]
        return df

    def report(self) -> None:
        for bb_report in self._bb_reports:
            bb_report.clear()

        for flow in self._flows:
            for bb_report in self._bb_reports:
                bb_report.add_flow(flow)

        for bb_report in self._bb_reports:
            bb_report.render(
                ByteBlower.InstanceGet().APIVersionGet(), version,
                self._port_list(), self._start_timestamp, self._end_timestamp
            )

            report_file_url = bb_report.report_url
            logging.info(
                'Stored report for %s to %r', bb_report, report_file_url
            )

    def _get_flow_run_time(self, flow: Flow) -> timedelta:
        """Return longest flow duration.

        :return: longest flow duration.
        :rtype: timedelta
        """
        try:
            return flow.initial_time_to_wait + flow.duration
        except (NotDurationBased, InfiniteDuration):
            return timedelta()
