#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_name import report_name as report_name_cls
from .new_report_name import new_report_name as new_report_name_cls
class rename_simulation_report(Command):
    """
    Rename a report which has already been generated.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        new_report_name : str
            'new_report_name' child.
    
    """

    fluent_name = "rename-simulation-report"

    argument_names = \
        ['report_name', 'new_report_name']

    report_name: report_name_cls = report_name_cls
    """
    report_name argument of rename_simulation_report.
    """
    new_report_name: new_report_name_cls = new_report_name_cls
    """
    new_report_name argument of rename_simulation_report.
    """
