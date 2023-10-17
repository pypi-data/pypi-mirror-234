#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .controls import controls as controls_cls
from .methods_1 import methods as methods_cls
from .report_definitions import report_definitions as report_definitions_cls
from .initialization import initialization as initialization_cls
from .run_calculation import run_calculation as run_calculation_cls
class solution(Group):
    """
    'solution' child.
    """

    fluent_name = "solution"

    child_names = \
        ['controls', 'methods', 'report_definitions', 'initialization',
         'run_calculation']

    controls: controls_cls = controls_cls
    """
    controls child of solution.
    """
    methods: methods_cls = methods_cls
    """
    methods child of solution.
    """
    report_definitions: report_definitions_cls = report_definitions_cls
    """
    report_definitions child of solution.
    """
    initialization: initialization_cls = initialization_cls
    """
    initialization child of solution.
    """
    run_calculation: run_calculation_cls = run_calculation_cls
    """
    run_calculation child of solution.
    """
