#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .scalar_parameters import scalar_parameters as scalar_parameters_cls
from .coupled_parameters import coupled_parameters as coupled_parameters_cls
from .flexible_cycle_parameters import flexible_cycle_parameters as flexible_cycle_parameters_cls
from .options_2 import options as options_cls
class amg_controls(Group):
    """
    'amg_controls' child.
    """

    fluent_name = "amg-controls"

    child_names = \
        ['scalar_parameters', 'coupled_parameters',
         'flexible_cycle_parameters', 'options']

    scalar_parameters: scalar_parameters_cls = scalar_parameters_cls
    """
    scalar_parameters child of amg_controls.
    """
    coupled_parameters: coupled_parameters_cls = coupled_parameters_cls
    """
    coupled_parameters child of amg_controls.
    """
    flexible_cycle_parameters: flexible_cycle_parameters_cls = flexible_cycle_parameters_cls
    """
    flexible_cycle_parameters child of amg_controls.
    """
    options: options_cls = options_cls
    """
    options child of amg_controls.
    """
