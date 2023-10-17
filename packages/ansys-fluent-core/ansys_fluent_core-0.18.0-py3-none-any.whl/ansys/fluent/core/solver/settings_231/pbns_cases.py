#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .flux_auto_select import flux_auto_select as flux_auto_select_cls
from .flux_type_1 import flux_type as flux_type_cls
class pbns_cases(Group):
    """
    'pbns_cases' child.
    """

    fluent_name = "pbns_cases"

    child_names = \
        ['flux_auto_select', 'flux_type']

    flux_auto_select: flux_auto_select_cls = flux_auto_select_cls
    """
    flux_auto_select child of pbns_cases.
    """
    flux_type: flux_type_cls = flux_type_cls
    """
    flux_type child of pbns_cases.
    """
