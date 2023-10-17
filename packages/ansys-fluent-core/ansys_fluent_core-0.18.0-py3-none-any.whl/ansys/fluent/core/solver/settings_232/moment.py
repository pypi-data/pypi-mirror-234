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
from .moment_child import moment_child

class moment(NamedObject[moment_child], _CreatableNamedObjectMixin[moment_child]):
    """
    'moment' child.
    """

    fluent_name = "moment"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of moment.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of moment.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of moment.
    """
    child_object_type: moment_child = moment_child
    """
    child_object_type of moment.
    """
