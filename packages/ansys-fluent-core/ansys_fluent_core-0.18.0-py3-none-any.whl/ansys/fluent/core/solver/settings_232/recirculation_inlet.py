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
from .recirculation_inlet_child import recirculation_inlet_child

class recirculation_inlet(NamedObject[recirculation_inlet_child], _NonCreatableNamedObjectMixin[recirculation_inlet_child]):
    """
    'recirculation_inlet' child.
    """

    fluent_name = "recirculation-inlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of recirculation_inlet.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of recirculation_inlet.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of recirculation_inlet.
    """
    child_object_type: recirculation_inlet_child = recirculation_inlet_child
    """
    child_object_type of recirculation_inlet.
    """
