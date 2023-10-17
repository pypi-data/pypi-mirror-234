#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .child_object_type_child_1 import child_object_type_child

class flux_momentum(ListObject[child_object_type_child]):
    """
    'flux_momentum' child.
    """

    fluent_name = "flux-momentum"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of flux_momentum.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of flux_momentum.
    """
