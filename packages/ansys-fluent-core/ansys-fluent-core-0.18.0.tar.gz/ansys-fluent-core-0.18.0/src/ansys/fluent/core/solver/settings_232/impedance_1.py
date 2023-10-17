#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .impedance_1_child import impedance_1_child

class impedance_1(ListObject[impedance_1_child]):
    """
    'impedance_1' child.
    """

    fluent_name = "impedance-1"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of impedance_1.
    """
    child_object_type: impedance_1_child = impedance_1_child
    """
    child_object_type of impedance_1.
    """
