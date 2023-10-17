#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use import use as use_cls
from .user_defined_2 import user_defined as user_defined_cls
from .value import value as value_cls
class vof_free_surface_weight(Group):
    """
    Set VOF free surface weight.
    """

    fluent_name = "vof-free-surface-weight"

    child_names = \
        ['use', 'user_defined', 'value']

    use: use_cls = use_cls
    """
    use child of vof_free_surface_weight.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of vof_free_surface_weight.
    """
    value: value_cls = value_cls
    """
    value child of vof_free_surface_weight.
    """
