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
from .flexible_cycle_paramters import flexible_cycle_paramters as flexible_cycle_paramters_cls
from .options_1 import options as options_cls
class algebric_mg_controls(Group):
    """
    'algebric_mg_controls' child.
    """

    fluent_name = "algebric-mg-controls"

    child_names = \
        ['scalar_parameters', 'coupled_parameters',
         'flexible_cycle_paramters', 'options']

    scalar_parameters: scalar_parameters_cls = scalar_parameters_cls
    """
    scalar_parameters child of algebric_mg_controls.
    """
    coupled_parameters: coupled_parameters_cls = coupled_parameters_cls
    """
    coupled_parameters child of algebric_mg_controls.
    """
    flexible_cycle_paramters: flexible_cycle_paramters_cls = flexible_cycle_paramters_cls
    """
    flexible_cycle_paramters child of algebric_mg_controls.
    """
    options: options_cls = options_cls
    """
    options child of algebric_mg_controls.
    """
