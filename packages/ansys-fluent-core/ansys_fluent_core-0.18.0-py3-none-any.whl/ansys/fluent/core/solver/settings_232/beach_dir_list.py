#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .beach_dir_list_child import beach_dir_list_child

class beach_dir_list(ListObject[beach_dir_list_child]):
    """
    'beach_dir_list' child.
    """

    fluent_name = "beach-dir-list"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of beach_dir_list.
    """
    child_object_type: beach_dir_list_child = beach_dir_list_child
    """
    child_object_type of beach_dir_list.
    """
