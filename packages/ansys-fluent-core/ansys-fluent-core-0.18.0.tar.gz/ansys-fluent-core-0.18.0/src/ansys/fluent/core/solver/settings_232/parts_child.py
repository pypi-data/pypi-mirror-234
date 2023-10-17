#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .bodies import bodies as bodies_cls
from .groups import groups as groups_cls
class parts_child(Group):
    """
    'child_object_type' of parts.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['bodies', 'groups']

    bodies: bodies_cls = bodies_cls
    """
    bodies child of parts_child.
    """
    groups: groups_cls = groups_cls
    """
    groups child of parts_child.
    """
