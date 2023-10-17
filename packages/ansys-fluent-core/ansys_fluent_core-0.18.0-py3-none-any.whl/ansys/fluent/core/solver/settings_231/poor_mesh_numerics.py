#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .set_1 import set as set_cls
from .list_properties_2 import list_properties as list_properties_cls
class poor_mesh_numerics(Group):
    """
    'poor_mesh_numerics' child.
    """

    fluent_name = "poor-mesh-numerics"

    child_names = \
        ['set']

    set: set_cls = set_cls
    """
    set child of poor_mesh_numerics.
    """
    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of poor_mesh_numerics.
    """
