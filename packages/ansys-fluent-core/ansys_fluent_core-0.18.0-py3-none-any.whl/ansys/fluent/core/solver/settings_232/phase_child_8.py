#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'is_not_a_rans_les_interface']

    name: name_cls = name_cls
    """
    name child of phase_child.
    """
    is_not_a_rans_les_interface: is_not_a_rans_les_interface_cls = is_not_a_rans_les_interface_cls
    """
    is_not_a_rans_les_interface child of phase_child.
    """
