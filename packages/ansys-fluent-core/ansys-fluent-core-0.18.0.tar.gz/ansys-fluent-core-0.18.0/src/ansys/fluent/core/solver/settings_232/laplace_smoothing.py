#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_2 import enabled as enabled_cls
from .set_2 import set as set_cls
class laplace_smoothing(Group):
    """
    'laplace_smoothing' child.
    """

    fluent_name = "laplace-smoothing"

    child_names = \
        ['enabled', 'set']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of laplace_smoothing.
    """
    set: set_cls = set_cls
    """
    set child of laplace_smoothing.
    """
