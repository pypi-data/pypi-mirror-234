#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .buoyancy_force_linearization import buoyancy_force_linearization as buoyancy_force_linearization_cls
from .blended_treatment_for_buoyancy_forces import blended_treatment_for_buoyancy_forces as blended_treatment_for_buoyancy_forces_cls
class coupled_vof(Group):
    """
    'coupled_vof' child.
    """

    fluent_name = "coupled-vof"

    child_names = \
        ['buoyancy_force_linearization',
         'blended_treatment_for_buoyancy_forces']

    buoyancy_force_linearization: buoyancy_force_linearization_cls = buoyancy_force_linearization_cls
    """
    buoyancy_force_linearization child of coupled_vof.
    """
    blended_treatment_for_buoyancy_forces: blended_treatment_for_buoyancy_forces_cls = blended_treatment_for_buoyancy_forces_cls
    """
    blended_treatment_for_buoyancy_forces child of coupled_vof.
    """
