#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .moving_mesh_cfl_constraint import moving_mesh_cfl_constraint as moving_mesh_cfl_constraint_cls
from .physics_based_constraint import physics_based_constraint as physics_based_constraint_cls
from .time_scale_options import time_scale_options as time_scale_options_cls
from .verbosity_11 import verbosity as verbosity_cls
class multiphase_specific_time_constraints(Group):
    """
    'multiphase_specific_time_constraints' child.
    """

    fluent_name = "multiphase-specific-time-constraints"

    child_names = \
        ['moving_mesh_cfl_constraint', 'physics_based_constraint',
         'time_scale_options', 'verbosity']

    moving_mesh_cfl_constraint: moving_mesh_cfl_constraint_cls = moving_mesh_cfl_constraint_cls
    """
    moving_mesh_cfl_constraint child of multiphase_specific_time_constraints.
    """
    physics_based_constraint: physics_based_constraint_cls = physics_based_constraint_cls
    """
    physics_based_constraint child of multiphase_specific_time_constraints.
    """
    time_scale_options: time_scale_options_cls = time_scale_options_cls
    """
    time_scale_options child of multiphase_specific_time_constraints.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of multiphase_specific_time_constraints.
    """
