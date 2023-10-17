import importlib.util

from . import roll_pass
from . import transport

VERSION = "2.1.0"

REPORT_INSTALLED = bool(importlib.util.find_spec("pyroll.report"))

if REPORT_INSTALLED:
    from . import report
    from pyroll.report import plugin_manager

    plugin_manager.register(report)

from pyroll.core import root_hooks, Unit

root_hooks.add(Unit.OutProfile.temperature)
