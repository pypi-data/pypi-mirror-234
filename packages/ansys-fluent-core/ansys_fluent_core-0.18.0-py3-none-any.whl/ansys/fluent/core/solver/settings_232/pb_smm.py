#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .child_object_type_child_1 import child_object_type_child

class pb_smm(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'pb_smm' child.
    """

    fluent_name = "pb-smm"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of pb_smm.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of pb_smm.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of pb_smm.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_smm.
    """
