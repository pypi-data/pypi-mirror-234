#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .periodic_child import periodic_child

class periodic(NamedObject[periodic_child], _CreatableNamedObjectMixin[periodic_child]):
    """
    'periodic' child.
    """

    fluent_name = "periodic"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of periodic.
    """
    child_object_type: periodic_child = periodic_child
    """
    child_object_type of periodic.
    """
