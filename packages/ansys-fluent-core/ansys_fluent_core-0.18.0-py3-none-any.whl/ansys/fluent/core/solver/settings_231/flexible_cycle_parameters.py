#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .max_fine_relaxations import max_fine_relaxations as max_fine_relaxations_cls
from .max_coarse_relaxations import max_coarse_relaxations as max_coarse_relaxations_cls
class flexible_cycle_parameters(Group):
    """
    'flexible_cycle_parameters' child.
    """

    fluent_name = "flexible-cycle-parameters"

    child_names = \
        ['max_fine_relaxations', 'max_coarse_relaxations']

    max_fine_relaxations: max_fine_relaxations_cls = max_fine_relaxations_cls
    """
    max_fine_relaxations child of flexible_cycle_parameters.
    """
    max_coarse_relaxations: max_coarse_relaxations_cls = max_coarse_relaxations_cls
    """
    max_coarse_relaxations child of flexible_cycle_parameters.
    """
