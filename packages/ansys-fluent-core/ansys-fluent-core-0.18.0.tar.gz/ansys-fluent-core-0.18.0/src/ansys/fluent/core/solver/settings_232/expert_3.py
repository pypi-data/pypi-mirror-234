#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .under_relaxation_factor import under_relaxation_factor as under_relaxation_factor_cls
from .explicit_relaxation_factor import explicit_relaxation_factor as explicit_relaxation_factor_cls
class expert(Group):
    """
    Enter menu for expert controls.
    """

    fluent_name = "expert"

    child_names = \
        ['under_relaxation_factor', 'explicit_relaxation_factor']

    under_relaxation_factor: under_relaxation_factor_cls = under_relaxation_factor_cls
    """
    under_relaxation_factor child of expert.
    """
    explicit_relaxation_factor: explicit_relaxation_factor_cls = explicit_relaxation_factor_cls
    """
    explicit_relaxation_factor child of expert.
    """
