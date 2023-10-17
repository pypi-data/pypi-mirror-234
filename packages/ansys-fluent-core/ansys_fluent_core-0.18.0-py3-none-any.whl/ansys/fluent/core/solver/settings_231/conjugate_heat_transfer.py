#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_3 import enabled as enabled_cls
from .set_5 import set as set_cls
class conjugate_heat_transfer(Group):
    """
    'conjugate_heat_transfer' child.
    """

    fluent_name = "conjugate-heat-transfer"

    child_names = \
        ['enabled', 'set']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of conjugate_heat_transfer.
    """
    set: set_cls = set_cls
    """
    set child of conjugate_heat_transfer.
    """
