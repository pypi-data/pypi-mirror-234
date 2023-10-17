#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .wave_list_child import wave_list_child

class wave_list(ListObject[wave_list_child]):
    """
    'wave_list' child.
    """

    fluent_name = "wave-list"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of wave_list.
    """
    child_object_type: wave_list_child = wave_list_child
    """
    child_object_type of wave_list.
    """
