#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .efficiency_function import efficiency_function as efficiency_function_cls
from .number_of_points_in_flame import number_of_points_in_flame as number_of_points_in_flame_cls
from .integral_length_scale import integral_length_scale as integral_length_scale_cls
from .sensor_method import sensor_method as sensor_method_cls
from .sensor_reaction_index import sensor_reaction_index as sensor_reaction_index_cls
from .beta_factor_omega_equation import beta_factor_omega_equation as beta_factor_omega_equation_cls
from .sensor_num_smooths import sensor_num_smooths as sensor_num_smooths_cls
class tfm_model_options(Group):
    """
    'tfm_model_options' child.
    """

    fluent_name = "tfm-model-options"

    child_names = \
        ['efficiency_function', 'number_of_points_in_flame',
         'integral_length_scale', 'sensor_method', 'sensor_reaction_index',
         'beta_factor_omega_equation', 'sensor_num_smooths']

    efficiency_function: efficiency_function_cls = efficiency_function_cls
    """
    efficiency_function child of tfm_model_options.
    """
    number_of_points_in_flame: number_of_points_in_flame_cls = number_of_points_in_flame_cls
    """
    number_of_points_in_flame child of tfm_model_options.
    """
    integral_length_scale: integral_length_scale_cls = integral_length_scale_cls
    """
    integral_length_scale child of tfm_model_options.
    """
    sensor_method: sensor_method_cls = sensor_method_cls
    """
    sensor_method child of tfm_model_options.
    """
    sensor_reaction_index: sensor_reaction_index_cls = sensor_reaction_index_cls
    """
    sensor_reaction_index child of tfm_model_options.
    """
    beta_factor_omega_equation: beta_factor_omega_equation_cls = beta_factor_omega_equation_cls
    """
    beta_factor_omega_equation child of tfm_model_options.
    """
    sensor_num_smooths: sensor_num_smooths_cls = sensor_num_smooths_cls
    """
    sensor_num_smooths child of tfm_model_options.
    """
