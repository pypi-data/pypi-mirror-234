#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .input_parameters import input_parameters as input_parameters_cls
from .output_parameters import output_parameters as output_parameters_cls
from .write_data_1 import write_data as write_data_cls
from .capture_simulation_report_data_1 import capture_simulation_report_data as capture_simulation_report_data_cls
class design_points_child(Group):
    """
    'child_object_type' of design_points.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['input_parameters', 'output_parameters', 'write_data',
         'capture_simulation_report_data']

    input_parameters: input_parameters_cls = input_parameters_cls
    """
    input_parameters child of design_points_child.
    """
    output_parameters: output_parameters_cls = output_parameters_cls
    """
    output_parameters child of design_points_child.
    """
    write_data: write_data_cls = write_data_cls
    """
    write_data child of design_points_child.
    """
    capture_simulation_report_data: capture_simulation_report_data_cls = capture_simulation_report_data_cls
    """
    capture_simulation_report_data child of design_points_child.
    """
