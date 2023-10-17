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
from .mesh_child import mesh_child

class mesh(NamedObject[mesh_child], _CreatableNamedObjectMixin[mesh_child]):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of mesh.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of mesh.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of mesh.
    """
    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
