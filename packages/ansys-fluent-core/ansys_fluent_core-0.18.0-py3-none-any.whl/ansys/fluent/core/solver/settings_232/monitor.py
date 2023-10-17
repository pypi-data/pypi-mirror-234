#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_files import report_files as report_files_cls
from .report_plots import report_plots as report_plots_cls
from .convergence_conditions import convergence_conditions as convergence_conditions_cls
class monitor(Group):
    """
    'monitor' child.
    """

    fluent_name = "monitor"

    child_names = \
        ['report_files', 'report_plots', 'convergence_conditions']

    report_files: report_files_cls = report_files_cls
    """
    report_files child of monitor.
    """
    report_plots: report_plots_cls = report_plots_cls
    """
    report_plots child of monitor.
    """
    convergence_conditions: convergence_conditions_cls = convergence_conditions_cls
    """
    convergence_conditions child of monitor.
    """
