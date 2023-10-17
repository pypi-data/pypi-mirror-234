#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cycle_type import cycle_type as cycle_type_cls
from .termination_criteria import termination_criteria as termination_criteria_cls
from .residual_reduction_tolerance import residual_reduction_tolerance as residual_reduction_tolerance_cls
from .method import method as method_cls
from .stabilization import stabilization as stabilization_cls
class multi_grid_controls_child(Group):
    """
    'child_object_type' of multi_grid_controls.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['cycle_type', 'termination_criteria', 'residual_reduction_tolerance',
         'method', 'stabilization']

    cycle_type: cycle_type_cls = cycle_type_cls
    """
    cycle_type child of multi_grid_controls_child.
    """
    termination_criteria: termination_criteria_cls = termination_criteria_cls
    """
    termination_criteria child of multi_grid_controls_child.
    """
    residual_reduction_tolerance: residual_reduction_tolerance_cls = residual_reduction_tolerance_cls
    """
    residual_reduction_tolerance child of multi_grid_controls_child.
    """
    method: method_cls = method_cls
    """
    method child of multi_grid_controls_child.
    """
    stabilization: stabilization_cls = stabilization_cls
    """
    stabilization child of multi_grid_controls_child.
    """
