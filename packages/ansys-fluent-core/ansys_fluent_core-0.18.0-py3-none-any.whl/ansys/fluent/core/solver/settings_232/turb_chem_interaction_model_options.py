#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .chemistry_iterations import chemistry_iterations as chemistry_iterations_cls
from .aggresiveness_factor import aggresiveness_factor as aggresiveness_factor_cls
from .transport_time_scale_factor import transport_time_scale_factor as transport_time_scale_factor_cls
from .min_temperature import min_temperature as min_temperature_cls
class turb_chem_interaction_model_options(Group):
    """
    'turb_chem_interaction_model_options' child.
    """

    fluent_name = "turb-chem-interaction-model-options"

    child_names = \
        ['chemistry_iterations', 'aggresiveness_factor',
         'transport_time_scale_factor', 'min_temperature']

    chemistry_iterations: chemistry_iterations_cls = chemistry_iterations_cls
    """
    chemistry_iterations child of turb_chem_interaction_model_options.
    """
    aggresiveness_factor: aggresiveness_factor_cls = aggresiveness_factor_cls
    """
    aggresiveness_factor child of turb_chem_interaction_model_options.
    """
    transport_time_scale_factor: transport_time_scale_factor_cls = transport_time_scale_factor_cls
    """
    transport_time_scale_factor child of turb_chem_interaction_model_options.
    """
    min_temperature: min_temperature_cls = min_temperature_cls
    """
    min_temperature child of turb_chem_interaction_model_options.
    """
