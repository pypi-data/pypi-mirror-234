#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .growth_ratio import growth_ratio as growth_ratio_cls
class growth_ratio_refinement(Group):
    """
    'growth_ratio_refinement' child.
    """

    fluent_name = "growth-ratio-refinement"

    child_names = \
        ['growth_ratio']

    growth_ratio: growth_ratio_cls = growth_ratio_cls
    """
    growth_ratio child of growth_ratio_refinement.
    """
