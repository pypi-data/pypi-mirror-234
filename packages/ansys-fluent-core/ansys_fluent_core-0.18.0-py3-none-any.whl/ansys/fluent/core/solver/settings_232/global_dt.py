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
from .local_dt_child import local_dt_child

class global_dt(NamedObject[local_dt_child], _NonCreatableNamedObjectMixin[local_dt_child]):
    """
    'global_dt' child.
    """

    fluent_name = "global-dt"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of global_dt.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of global_dt.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of global_dt.
    """
    child_object_type: local_dt_child = local_dt_child
    """
    child_object_type of global_dt.
    """
