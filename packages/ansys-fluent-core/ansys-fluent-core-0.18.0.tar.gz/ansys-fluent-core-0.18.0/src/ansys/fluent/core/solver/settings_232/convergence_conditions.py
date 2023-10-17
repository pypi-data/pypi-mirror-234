#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .convergence_reports import convergence_reports as convergence_reports_cls
from .frequency_1 import frequency as frequency_cls
from .condition import condition as condition_cls
from .check_for import check_for as check_for_cls
class convergence_conditions(Group):
    """
    'convergence_conditions' child.
    """

    fluent_name = "convergence-conditions"

    child_names = \
        ['convergence_reports', 'frequency', 'condition', 'check_for']

    convergence_reports: convergence_reports_cls = convergence_reports_cls
    """
    convergence_reports child of convergence_conditions.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of convergence_conditions.
    """
    condition: condition_cls = condition_cls
    """
    condition child of convergence_conditions.
    """
    check_for: check_for_cls = check_for_cls
    """
    check_for child of convergence_conditions.
    """
