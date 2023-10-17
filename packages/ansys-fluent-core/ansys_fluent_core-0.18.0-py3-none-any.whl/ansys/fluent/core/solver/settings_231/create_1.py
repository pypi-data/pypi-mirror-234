#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .write_data import write_data as write_data_cls
from .capture_simulation_report_data import capture_simulation_report_data as capture_simulation_report_data_cls
class create_1(Command):
    """
    Add new Design Point.
    
    Parameters
    ----------
        write_data : bool
            'write_data' child.
        capture_simulation_report_data : bool
            'capture_simulation_report_data' child.
    
    """

    fluent_name = "create"

    argument_names = \
        ['write_data', 'capture_simulation_report_data']

    write_data: write_data_cls = write_data_cls
    """
    write_data argument of create_1.
    """
    capture_simulation_report_data: capture_simulation_report_data_cls = capture_simulation_report_data_cls
    """
    capture_simulation_report_data argument of create_1.
    """
