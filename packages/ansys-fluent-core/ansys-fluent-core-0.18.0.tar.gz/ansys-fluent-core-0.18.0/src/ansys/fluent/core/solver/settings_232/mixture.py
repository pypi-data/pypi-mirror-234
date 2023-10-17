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
from .mixture_child import mixture_child

class mixture(NamedObject[mixture_child], _CreatableNamedObjectMixin[mixture_child]):
    """
    'mixture' child.
    """

    fluent_name = "mixture"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of mixture.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of mixture.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of mixture.
    """
    child_object_type: mixture_child = mixture_child
    """
    child_object_type of mixture.
    """
