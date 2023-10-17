#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .dbns_cases import dbns_cases as dbns_cases_cls
from .pbns_cases import pbns_cases as pbns_cases_cls
class flux_type(Group):
    """
    Enter the flux type.
    """

    fluent_name = "flux-type"

    child_names = \
        ['dbns_cases', 'pbns_cases']

    dbns_cases: dbns_cases_cls = dbns_cases_cls
    """
    dbns_cases child of flux_type.
    """
    pbns_cases: pbns_cases_cls = pbns_cases_cls
    """
    pbns_cases child of flux_type.
    """
