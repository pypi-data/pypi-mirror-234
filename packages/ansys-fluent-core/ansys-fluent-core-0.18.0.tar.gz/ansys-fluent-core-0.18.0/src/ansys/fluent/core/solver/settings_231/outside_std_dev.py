#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .lower import lower as lower_cls
from .upper import upper as upper_cls
class outside_std_dev(Group):
    """
    'outside_std_dev' child.
    """

    fluent_name = "outside-std-dev"

    child_names = \
        ['lower', 'upper']

    lower: lower_cls = lower_cls
    """
    lower child of outside_std_dev.
    """
    upper: upper_cls = upper_cls
    """
    upper child of outside_std_dev.
    """
