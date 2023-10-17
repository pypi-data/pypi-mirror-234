#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .coefficient import coefficient as coefficient_cls
from .update_dissipation import update_dissipation as update_dissipation_cls
from .update_viscous import update_viscous as update_viscous_cls
class multi_stage_child(Group):
    """
    'child_object_type' of multi_stage.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'update_dissipation', 'update_viscous']

    coefficient: coefficient_cls = coefficient_cls
    """
    coefficient child of multi_stage_child.
    """
    update_dissipation: update_dissipation_cls = update_dissipation_cls
    """
    update_dissipation child of multi_stage_child.
    """
    update_viscous: update_viscous_cls = update_viscous_cls
    """
    update_viscous child of multi_stage_child.
    """
