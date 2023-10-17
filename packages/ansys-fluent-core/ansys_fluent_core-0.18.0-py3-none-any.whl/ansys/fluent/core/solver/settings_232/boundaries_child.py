#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_4 import type as type_cls
from .locations import locations as locations_cls
class boundaries_child(Group):
    """
    'child_object_type' of boundaries.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'locations']

    type: type_cls = type_cls
    """
    type child of boundaries_child.
    """
    locations: locations_cls = locations_cls
    """
    locations child of boundaries_child.
    """
