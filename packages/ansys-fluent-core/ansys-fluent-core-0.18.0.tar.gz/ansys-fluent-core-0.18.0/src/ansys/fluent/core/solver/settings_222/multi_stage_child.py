#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .coefficient import coefficient as coefficient_cls
from .dissipation import dissipation as dissipation_cls
from .viscous_1 import viscous as viscous_cls
class multi_stage_child(Group):
    """
    'child_object_type' of multi_stage.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'dissipation', 'viscous']

    coefficient: coefficient_cls = coefficient_cls
    """
    coefficient child of multi_stage_child.
    """
    dissipation: dissipation_cls = dissipation_cls
    """
    dissipation child of multi_stage_child.
    """
    viscous: viscous_cls = viscous_cls
    """
    viscous child of multi_stage_child.
    """
