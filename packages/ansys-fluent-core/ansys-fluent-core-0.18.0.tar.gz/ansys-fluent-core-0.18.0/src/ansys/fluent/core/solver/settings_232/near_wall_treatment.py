#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .wall_treatment import wall_treatment as wall_treatment_cls
from .user_defined import user_defined as user_defined_cls
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options as enhanced_wall_treatment_options_cls
from .wall_omega_treatment import wall_omega_treatment as wall_omega_treatment_cls
class near_wall_treatment(Group):
    """
    'near_wall_treatment' child.
    """

    fluent_name = "near-wall-treatment"

    child_names = \
        ['wall_treatment', 'user_defined', 'enhanced_wall_treatment_options',
         'wall_omega_treatment']

    wall_treatment: wall_treatment_cls = wall_treatment_cls
    """
    wall_treatment child of near_wall_treatment.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of near_wall_treatment.
    """
    enhanced_wall_treatment_options: enhanced_wall_treatment_options_cls = enhanced_wall_treatment_options_cls
    """
    enhanced_wall_treatment_options child of near_wall_treatment.
    """
    wall_omega_treatment: wall_omega_treatment_cls = wall_omega_treatment_cls
    """
    wall_omega_treatment child of near_wall_treatment.
    """
