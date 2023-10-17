#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .components_2 import components as components_cls
from .list_properties_4 import list_properties as list_properties_cls
class groups_child(Group):
    """
    'child_object_type' of groups.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['components']

    components: components_cls = components_cls
    """
    components child of groups_child.
    """
    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of groups_child.
    """
