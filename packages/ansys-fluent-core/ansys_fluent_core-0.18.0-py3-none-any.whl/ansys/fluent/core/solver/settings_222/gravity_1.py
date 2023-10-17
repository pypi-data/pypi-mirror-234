#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .gravity import gravity as gravity_cls
from .components import components as components_cls
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['gravity', 'components']

    gravity: gravity_cls = gravity_cls
    """
    gravity child of gravity.
    """
    components: components_cls = components_cls
    """
    components child of gravity.
    """
