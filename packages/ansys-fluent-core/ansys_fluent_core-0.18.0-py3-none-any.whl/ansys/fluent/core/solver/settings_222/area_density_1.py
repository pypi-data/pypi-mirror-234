#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .vof_min_seeding import vof_min_seeding as vof_min_seeding_cls
from .ia_grad_sym import ia_grad_sym as ia_grad_sym_cls
class area_density(Group):
    """
    'area_density' child.
    """

    fluent_name = "area-density"

    child_names = \
        ['vof_min_seeding', 'ia_grad_sym']

    vof_min_seeding: vof_min_seeding_cls = vof_min_seeding_cls
    """
    vof_min_seeding child of area_density.
    """
    ia_grad_sym: ia_grad_sym_cls = ia_grad_sym_cls
    """
    ia_grad_sym child of area_density.
    """
