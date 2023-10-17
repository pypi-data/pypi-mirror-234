#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .rich_equivalence_ratio_limit import rich_equivalence_ratio_limit as rich_equivalence_ratio_limit_cls
from .exponential_factor_beta import exponential_factor_beta as exponential_factor_beta_cls
class equilibrium_rich_flammability_options(Group):
    """
    'equilibrium_rich_flammability_options' child.
    """

    fluent_name = "equilibrium-rich-flammability-options"

    child_names = \
        ['rich_equivalence_ratio_limit', 'exponential_factor_beta']

    rich_equivalence_ratio_limit: rich_equivalence_ratio_limit_cls = rich_equivalence_ratio_limit_cls
    """
    rich_equivalence_ratio_limit child of equilibrium_rich_flammability_options.
    """
    exponential_factor_beta: exponential_factor_beta_cls = exponential_factor_beta_cls
    """
    exponential_factor_beta child of equilibrium_rich_flammability_options.
    """
