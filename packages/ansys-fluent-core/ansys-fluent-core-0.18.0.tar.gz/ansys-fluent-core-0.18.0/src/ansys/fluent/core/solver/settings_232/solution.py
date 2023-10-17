#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .methods import methods as methods_cls
from .controls_1 import controls as controls_cls
from .report_definitions import report_definitions as report_definitions_cls
from .monitor import monitor as monitor_cls
from .cell_registers import cell_registers as cell_registers_cls
from .initialization import initialization as initialization_cls
from .calculation_activity import calculation_activity as calculation_activity_cls
from .run_calculation import run_calculation as run_calculation_cls
class solution(Group):
    """
    'solution' child.
    """

    fluent_name = "solution"

    child_names = \
        ['methods', 'controls', 'report_definitions', 'monitor',
         'cell_registers', 'initialization', 'calculation_activity',
         'run_calculation']

    methods: methods_cls = methods_cls
    """
    methods child of solution.
    """
    controls: controls_cls = controls_cls
    """
    controls child of solution.
    """
    report_definitions: report_definitions_cls = report_definitions_cls
    """
    report_definitions child of solution.
    """
    monitor: monitor_cls = monitor_cls
    """
    monitor child of solution.
    """
    cell_registers: cell_registers_cls = cell_registers_cls
    """
    cell_registers child of solution.
    """
    initialization: initialization_cls = initialization_cls
    """
    initialization child of solution.
    """
    calculation_activity: calculation_activity_cls = calculation_activity_cls
    """
    calculation_activity child of solution.
    """
    run_calculation: run_calculation_cls = run_calculation_cls
    """
    run_calculation child of solution.
    """
