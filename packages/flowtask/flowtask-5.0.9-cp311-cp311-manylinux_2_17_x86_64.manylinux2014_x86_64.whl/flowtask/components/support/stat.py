from abc import ABC
from typing import Optional
import traceback
from flowtask.utils.stats import TaskMonitor


class StatSupport(ABC):
    """StatSupport.

    Adding Support for Task Monitor (Statistics Collector.)
    """
    def __init__(
            self,
            stat: Optional[TaskMonitor] = None
    ):
        # stats object:
        self._stat_: bool = True
        if stat:
            self.stat: Optional[TaskMonitor] = stat
        else:
            self.stat = None
            self._stat_ = False

    def save_traceback(self):
        try:
            self.stat.stacktrace(
                traceback.format_exc()
            )
        finally:
            pass

    def add_metric(self, name, value):
        try:
            self.stat.add_metric(name, value)
        except AttributeError:
            pass
