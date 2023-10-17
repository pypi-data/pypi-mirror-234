#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .convergence_acceleration_type import convergence_acceleration_type as convergence_acceleration_type_cls
from .casm_cutoff_multiplier import casm_cutoff_multiplier as casm_cutoff_multiplier_cls
class convergence_acceleration_for_stretched_meshes(Group):
    """
    Enable convergence acceleration for stretched meshes to improve the convergence of the implicit density based solver on meshes with high cell stretching.
    """

    fluent_name = "convergence-acceleration-for-stretched-meshes"

    child_names = \
        ['convergence_acceleration_type', 'casm_cutoff_multiplier']

    convergence_acceleration_type: convergence_acceleration_type_cls = convergence_acceleration_type_cls
    """
    convergence_acceleration_type child of convergence_acceleration_for_stretched_meshes.
    """
    casm_cutoff_multiplier: casm_cutoff_multiplier_cls = casm_cutoff_multiplier_cls
    """
    casm_cutoff_multiplier child of convergence_acceleration_for_stretched_meshes.
    """
