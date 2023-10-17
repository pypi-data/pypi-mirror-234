#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .shell_conduction_child import shell_conduction_child

class thin_wall(ListObject[shell_conduction_child]):
    """
    'thin_wall' child.
    """

    fluent_name = "thin-wall"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of thin_wall.
    """
    child_object_type: shell_conduction_child = shell_conduction_child
    """
    child_object_type of thin_wall.
    """
