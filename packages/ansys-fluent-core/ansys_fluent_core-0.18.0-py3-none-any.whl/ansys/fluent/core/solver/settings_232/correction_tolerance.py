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
from .correction_tolerance_child import correction_tolerance_child

class correction_tolerance(NamedObject[correction_tolerance_child], _NonCreatableNamedObjectMixin[correction_tolerance_child]):
    """
    'correction_tolerance' child.
    """

    fluent_name = "correction-tolerance"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of correction_tolerance.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of correction_tolerance.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of correction_tolerance.
    """
    child_object_type: correction_tolerance_child = correction_tolerance_child
    """
    child_object_type of correction_tolerance.
    """
