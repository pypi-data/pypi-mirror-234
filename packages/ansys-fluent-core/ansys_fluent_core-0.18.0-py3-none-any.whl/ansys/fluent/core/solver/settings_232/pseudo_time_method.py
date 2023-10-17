#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .formulation import formulation as formulation_cls
from .relaxation_method import relaxation_method as relaxation_method_cls
from .convergence_acceleration_for_stretched_meshes import convergence_acceleration_for_stretched_meshes as convergence_acceleration_for_stretched_meshes_cls
from .relaxation_bounds import relaxation_bounds as relaxation_bounds_cls
class pseudo_time_method(Group):
    """
    Enter the pseudo time method menu.
    """

    fluent_name = "pseudo-time-method"

    child_names = \
        ['formulation', 'relaxation_method',
         'convergence_acceleration_for_stretched_meshes']

    formulation: formulation_cls = formulation_cls
    """
    formulation child of pseudo_time_method.
    """
    relaxation_method: relaxation_method_cls = relaxation_method_cls
    """
    relaxation_method child of pseudo_time_method.
    """
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes_cls = convergence_acceleration_for_stretched_meshes_cls
    """
    convergence_acceleration_for_stretched_meshes child of pseudo_time_method.
    """
    command_names = \
        ['relaxation_bounds']

    relaxation_bounds: relaxation_bounds_cls = relaxation_bounds_cls
    """
    relaxation_bounds command of pseudo_time_method.
    """
