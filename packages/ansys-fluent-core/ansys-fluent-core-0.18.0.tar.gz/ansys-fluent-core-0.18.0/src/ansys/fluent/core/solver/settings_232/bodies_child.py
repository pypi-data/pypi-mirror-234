#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .faces import faces as faces_cls
from .list_properties_4 import list_properties as list_properties_cls
class bodies_child(Group):
    """
    'child_object_type' of bodies.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['faces']

    faces: faces_cls = faces_cls
    """
    faces child of bodies_child.
    """
    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of bodies_child.
    """
