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
from .copy import copy as copy_cls
from .beams_child import beams_child

class beams(NamedObject[beams_child], _CreatableNamedObjectMixin[beams_child]):
    """
    Enter the optical beams menu.
    """

    fluent_name = "beams"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'copy']

    list: list_cls = list_cls
    """
    list command of beams.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of beams.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of beams.
    """
    copy: copy_cls = copy_cls
    """
    copy command of beams.
    """
    child_object_type: beams_child = beams_child
    """
    child_object_type of beams.
    """
