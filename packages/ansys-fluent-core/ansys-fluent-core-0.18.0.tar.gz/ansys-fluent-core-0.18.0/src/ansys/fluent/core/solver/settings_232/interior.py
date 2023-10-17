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
from .interior_child import interior_child

class interior(NamedObject[interior_child], _NonCreatableNamedObjectMixin[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of interior.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of interior.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of interior.
    """
    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
