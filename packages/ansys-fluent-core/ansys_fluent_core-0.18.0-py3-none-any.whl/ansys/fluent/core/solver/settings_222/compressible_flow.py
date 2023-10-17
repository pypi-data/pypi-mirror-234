#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enhanced_numerics import enhanced_numerics as enhanced_numerics_cls
from .alternate_bc_formulation import alternate_bc_formulation as alternate_bc_formulation_cls
from .analytical_thermodynamic_derivatives import analytical_thermodynamic_derivatives as analytical_thermodynamic_derivatives_cls
class compressible_flow(Group):
    """
    'compressible_flow' child.
    """

    fluent_name = "compressible-flow"

    child_names = \
        ['enhanced_numerics', 'alternate_bc_formulation',
         'analytical_thermodynamic_derivatives']

    enhanced_numerics: enhanced_numerics_cls = enhanced_numerics_cls
    """
    enhanced_numerics child of compressible_flow.
    """
    alternate_bc_formulation: alternate_bc_formulation_cls = alternate_bc_formulation_cls
    """
    alternate_bc_formulation child of compressible_flow.
    """
    analytical_thermodynamic_derivatives: analytical_thermodynamic_derivatives_cls = analytical_thermodynamic_derivatives_cls
    """
    analytical_thermodynamic_derivatives child of compressible_flow.
    """
