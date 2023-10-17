#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_8 import phase as phase_cls
from .name_1 import name as name_cls
from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls
class interior_child(Group):
    """
    'child_object_type' of interior.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'name', 'is_not_a_rans_les_interface']

    phase: phase_cls = phase_cls
    """
    phase child of interior_child.
    """
    name: name_cls = name_cls
    """
    name child of interior_child.
    """
    is_not_a_rans_les_interface: is_not_a_rans_les_interface_cls = is_not_a_rans_les_interface_cls
    """
    is_not_a_rans_les_interface child of interior_child.
    """
