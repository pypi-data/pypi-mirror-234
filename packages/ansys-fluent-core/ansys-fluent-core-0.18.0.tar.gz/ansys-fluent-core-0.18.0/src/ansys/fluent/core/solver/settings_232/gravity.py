#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_2 import enable as enable_cls
from .components import components as components_cls
from .gravity_mrf_behavior import gravity_mrf_behavior as gravity_mrf_behavior_cls
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['enable', 'components', 'gravity_mrf_behavior']

    enable: enable_cls = enable_cls
    """
    enable child of gravity.
    """
    components: components_cls = components_cls
    """
    components child of gravity.
    """
    gravity_mrf_behavior: gravity_mrf_behavior_cls = gravity_mrf_behavior_cls
    """
    gravity_mrf_behavior child of gravity.
    """
