#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fixed_cycle_parameters_1 import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters_1 import coarsening_parameters as coarsening_parameters_cls
from .smoother_type_1 import smoother_type as smoother_type_cls
class coupled_parameters(Group):
    """
    'coupled_parameters' child.
    """

    fluent_name = "coupled-parameters"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters', 'smoother_type']

    fixed_cycle_parameters: fixed_cycle_parameters_cls = fixed_cycle_parameters_cls
    """
    fixed_cycle_parameters child of coupled_parameters.
    """
    coarsening_parameters: coarsening_parameters_cls = coarsening_parameters_cls
    """
    coarsening_parameters child of coupled_parameters.
    """
    smoother_type: smoother_type_cls = smoother_type_cls
    """
    smoother_type child of coupled_parameters.
    """
