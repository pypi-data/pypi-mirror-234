"""Helpers to support synchronized execution of certain functions."""
import logging
from typing import Any, Callable, Iterable, List  # for type hinting

from byteblowerll.byteblower import SchedulableObject  # for type hinting
from byteblowerll.byteblower import ScheduleGroup  # for type hinting

__all__ = (
    'SynchronizedExecutable',
    'SynchronizedExecution',
    'synchronized_start',
)

_LOGGER = logging.getLogger(__name__)


class SynchronizedExecutable(object):  # pylint: disable=too-few-public-methods
    """Executable which can be used for synchronized operations."""

    __slots__ = ('_schedulable_object', )

    def __init__(self, schedulable_object: SchedulableObject) -> None:
        """Create a synchronized executable.

        :param schedulable_object: Schedulable object. Can be used
           for example for synchronized start.
        :type schedulable_object: SchedulableObject
        """
        self._schedulable_object = schedulable_object

    @property
    def schedulable_object(self) -> SchedulableObject:
        """Return our schedulable object."""
        return self._schedulable_object


class SynchronizedExecution(object):
    """Performs synchronized operations on an synchronized executable."""

    __slots__ = ('_sync_executables', )

    def __init__(self) -> None:
        """Create the synchronized execution helper."""
        self._sync_executables: List[SynchronizedExecutable] = []

    def add(self, sync_exe_iter: Iterable[SynchronizedExecutable]) -> None:
        """Add synchronized executables.

        :param sync_exe_iter: Synchronized executable to add
        :type sync_exe_iter: Iterable[SynchronizedExecutable]
        """
        for sync_exe in sync_exe_iter:
            self._sync_executables.append(sync_exe.schedulable_object)

    def execute(self, func: Callable[[SchedulableObject], Any]) -> None:
        """Call the given function on our synchronized executables.

        :param func: Function to execute
        :type func: Callable[[SchedulableObject], Any]
        """
        func(self._sync_executables)


def synchronized_start(
    schedule_group: ScheduleGroup
) -> Callable[[SchedulableObject], Any]:
    """Create a synchronized start function for SchedulableObjects.

    The returned function can be used with :meth:`SynchronizedExecution.exec`.

    :param schedule_group: Schedule group to where ``SchedulableObject``s
       will be added to.
    :type schedule_group: ScheduleGroup
    :return: Function to perform a synchronized start on a
       list of :class:`SchedulableObject`s.
    :rtype: Callable[[SchedulableObject], Any]
    """

    def run_sync_start(schedulable_objects: Iterable[SchedulableObject]):
        for schedulable_object in schedulable_objects:
            _LOGGER.debug(
                'ScheduleGroup %r: Adding %r', schedule_group,
                schedulable_object
            )
            schedule_group.MembersAdd(schedulable_object)
        schedule_group.Prepare()
        schedule_group.Start()

    return run_sync_start
