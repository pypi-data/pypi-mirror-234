#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .first_rate import first_rate as first_rate_cls
from .second_rate import second_rate as second_rate_cls
class two_competing_rates(Group):
    """
    'two_competing_rates' child.
    """

    fluent_name = "two-competing-rates"

    child_names = \
        ['first_rate', 'second_rate']

    first_rate: first_rate_cls = first_rate_cls
    """
    first_rate child of two_competing_rates.
    """
    second_rate: second_rate_cls = second_rate_cls
    """
    second_rate child of two_competing_rates.
    """
