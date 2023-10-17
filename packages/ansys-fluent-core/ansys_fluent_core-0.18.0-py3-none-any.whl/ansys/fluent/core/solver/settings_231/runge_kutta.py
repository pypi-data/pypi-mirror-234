#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .two_stage import two_stage as two_stage_cls
from .default_multi_stage import default_multi_stage as default_multi_stage_cls
class runge_kutta(Group):
    """
    'runge_kutta' child.
    """

    fluent_name = "runge-kutta"

    child_names = \
        ['two_stage', 'default_multi_stage']

    two_stage: two_stage_cls = two_stage_cls
    """
    two_stage child of runge_kutta.
    """
    default_multi_stage: default_multi_stage_cls = default_multi_stage_cls
    """
    default_multi_stage child of runge_kutta.
    """
