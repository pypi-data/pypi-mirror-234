"""This file defines the methods to report test steps and failures."""
import time
from typing import List, Optional  # for type hinting

from junit_xml import TestCase, TestSuite


class UnitTestReport(object):
    """Helper for generating JUnit XML test reports."""

    __slots__ = (
        '_test_suite_list',
        '_test_case_list',
        '_current_subtest',
        '_subtest_counter',
    )

    def __init__(self) -> None:
        """Construct a new helper."""
        self._test_suite_list: List[TestSuite] = []
        self._test_case_list: List[TestCase] = []
        self._current_subtest: str = ''
        self._subtest_counter: int = 1

    def set_subtest(self, subtest: str) -> None:
        """
        Start a new subtest; known as a test suite in JUnit XML.

        .. note::
           The previous subtest will be closed.
           When it did not contain any test cases,
           it won't be added to the report.

        :param subtest: The subtest in the report
        """
        self._close_current_subtest()
        self._current_subtest = subtest

    def add_pass(
        self, step: str, message: str, stderr: Optional[str] = None
    ) -> None:
        """
        Add a succeeded test case.

        :param step: The step name (no spaces)
        :param message: The "pass" text (== test standard output / log)
        :param stdout: The test standard output (log)
        """
        test = TestCase(
            step,
            # NOTE: The testcase classname is used as "suite" name
            #       in the GitLab Unit test reporting.
            classname=self._current_subtest,
            stdout=message,
            stderr=stderr,
            timestamp=time.time(),
            status='success',
        )
        self._test_case_list.append(test)

    def add_fail(
        self, step: str, message: str, stdout: Optional[str] = None
    ) -> None:
        """
        Add a failed test case.

        :param step: The step name (no spaces)
        :param message: The "fail" text
        :param stdout: The test standard output (log)
        """
        test = TestCase(
            step,
            # NOTE: The testcase classname is used as "suite" name
            #       in the GitLab Unit test reporting.
            classname=self._current_subtest,
            stdout=stdout,
            timestamp=time.time(),
            status='failure',
        )
        test.add_failure_info(message=message)
        self._test_case_list.append(test)

    def add_skipped(
        self,
        step: str,
        message: str,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None
    ) -> None:
        """
        Add a skipped test case.

        :param step: The step name (no spaces)
        :param message: The "skipped" text
        :param stdout: The test standard output (log)
        :param stderr: The test standard error (failure log)
        """
        test = TestCase(
            step,
            # NOTE: The testcase classname is used as "suite" name
            #       in the GitLab Unit test reporting.
            classname=self._current_subtest,
            stdout=stdout,
            stderr=stderr,
            timestamp=time.time(),
            status='skipped',
        )
        test.add_skipped_info(message=message)
        self._test_case_list.append(test)

    def save(self, name: str = 'report.xml') -> None:
        """
        Write the JUnit XML file.

        This file can then be processed by the CI/CD/CT tool.

        :param name: Name of the JUnit XML output file.
        """
        self._close_current_subtest()
        with open(name, 'w', encoding='utf-8') as xml_report:
            TestSuite.to_file(xml_report, self._test_suite_list)

    def _close_current_subtest(self) -> None:
        if len(self._test_case_list) > 0:
            self._test_suite_list.append(
                TestSuite(
                    f'{self._subtest_counter!s}_ {self._current_subtest}',
                    test_cases=self._test_case_list,
                )
            )
            self._subtest_counter += 1
            self._test_case_list = []
