#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fixed_cycle_parameters_2 import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters_2 import coarsening_parameters as coarsening_parameters_cls
from .relaxation_factor_2 import relaxation_factor as relaxation_factor_cls
from .options_7 import options as options_cls
class fas_mg_controls(Group):
    """
    'fas_mg_controls' child.
    """

    fluent_name = "fas-mg-controls"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters',
         'relaxation_factor', 'options']

    fixed_cycle_parameters: fixed_cycle_parameters_cls = fixed_cycle_parameters_cls
    """
    fixed_cycle_parameters child of fas_mg_controls.
    """
    coarsening_parameters: coarsening_parameters_cls = coarsening_parameters_cls
    """
    coarsening_parameters child of fas_mg_controls.
    """
    relaxation_factor: relaxation_factor_cls = relaxation_factor_cls
    """
    relaxation_factor child of fas_mg_controls.
    """
    options: options_cls = options_cls
    """
    options child of fas_mg_controls.
    """
