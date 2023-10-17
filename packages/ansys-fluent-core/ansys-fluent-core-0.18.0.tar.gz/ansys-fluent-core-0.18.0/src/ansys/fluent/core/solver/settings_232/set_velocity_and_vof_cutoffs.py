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
from .set_velocity_and_vof_cutoffs_child import set_velocity_and_vof_cutoffs_child

class set_velocity_and_vof_cutoffs(NamedObject[set_velocity_and_vof_cutoffs_child], _NonCreatableNamedObjectMixin[set_velocity_and_vof_cutoffs_child]):
    """
    'set_velocity_and_vof_cutoffs' child.
    """

    fluent_name = "set-velocity-and-vof-cutoffs"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of set_velocity_and_vof_cutoffs.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of set_velocity_and_vof_cutoffs.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of set_velocity_and_vof_cutoffs.
    """
    child_object_type: set_velocity_and_vof_cutoffs_child = set_velocity_and_vof_cutoffs_child
    """
    child_object_type of set_velocity_and_vof_cutoffs.
    """
