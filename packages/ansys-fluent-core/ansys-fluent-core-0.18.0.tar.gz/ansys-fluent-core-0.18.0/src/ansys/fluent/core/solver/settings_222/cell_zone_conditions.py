#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fluid_1 import fluid as fluid_cls
from .solid_1 import solid as solid_cls
class cell_zone_conditions(Group):
    """
    'cell_zone_conditions' child.
    """

    fluent_name = "cell-zone-conditions"

    child_names = \
        ['fluid', 'solid']

    fluid: fluid_cls = fluid_cls
    """
    fluid child of cell_zone_conditions.
    """
    solid: solid_cls = solid_cls
    """
    solid child of cell_zone_conditions.
    """
