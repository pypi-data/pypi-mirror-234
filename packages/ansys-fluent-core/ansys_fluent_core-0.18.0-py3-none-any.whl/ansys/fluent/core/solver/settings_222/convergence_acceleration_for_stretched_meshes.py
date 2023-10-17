#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .convergence_acc_std_meshes import convergence_acc_std_meshes as convergence_acc_std_meshes_cls
from .enhanced_casm_formulation import enhanced_casm_formulation as enhanced_casm_formulation_cls
from .casm_cutoff_multiplier import casm_cutoff_multiplier as casm_cutoff_multiplier_cls
from .disable_casm import disable_casm as disable_casm_cls
class convergence_acceleration_for_stretched_meshes(Group):
    """
    'convergence_acceleration_for_stretched_meshes' child.
    """

    fluent_name = "convergence-acceleration-for-stretched-meshes"

    child_names = \
        ['convergence_acc_std_meshes', 'enhanced_casm_formulation',
         'casm_cutoff_multiplier']

    convergence_acc_std_meshes: convergence_acc_std_meshes_cls = convergence_acc_std_meshes_cls
    """
    convergence_acc_std_meshes child of convergence_acceleration_for_stretched_meshes.
    """
    enhanced_casm_formulation: enhanced_casm_formulation_cls = enhanced_casm_formulation_cls
    """
    enhanced_casm_formulation child of convergence_acceleration_for_stretched_meshes.
    """
    casm_cutoff_multiplier: casm_cutoff_multiplier_cls = casm_cutoff_multiplier_cls
    """
    casm_cutoff_multiplier child of convergence_acceleration_for_stretched_meshes.
    """
    command_names = \
        ['disable_casm']

    disable_casm: disable_casm_cls = disable_casm_cls
    """
    disable_casm command of convergence_acceleration_for_stretched_meshes.
    """
