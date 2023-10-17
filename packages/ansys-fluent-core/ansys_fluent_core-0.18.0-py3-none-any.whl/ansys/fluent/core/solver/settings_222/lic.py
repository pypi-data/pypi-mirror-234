#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display import display as display_cls
from .lic_child import lic_child

class lic(NamedObject[lic_child], _CreatableNamedObjectMixin[lic_child]):
    """
    'lic' child.
    """

    fluent_name = "lic"

    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of lic.
    """
    child_object_type: lic_child = lic_child
    """
    child_object_type of lic.
    """
