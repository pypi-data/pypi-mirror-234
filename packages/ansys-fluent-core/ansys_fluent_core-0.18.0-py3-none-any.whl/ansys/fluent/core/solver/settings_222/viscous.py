#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model import model as model_cls
from .options import options as options_cls
from .spalart_allmaras_production import spalart_allmaras_production as spalart_allmaras_production_cls
from .k_epsilon_model import k_epsilon_model as k_epsilon_model_cls
from .k_omega_model import k_omega_model as k_omega_model_cls
from .k_omega_options import k_omega_options as k_omega_options_cls
from .rng_options import rng_options as rng_options_cls
from .near_wall_treatment import near_wall_treatment as near_wall_treatment_cls
from .transition_sst_options import transition_sst_options as transition_sst_options_cls
from .reynolds_stress_model import reynolds_stress_model as reynolds_stress_model_cls
from .subgrid_scale_model import subgrid_scale_model as subgrid_scale_model_cls
from .les_model_options import les_model_options as les_model_options_cls
from .reynolds_stress_options import reynolds_stress_options as reynolds_stress_options_cls
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options as enhanced_wall_treatment_options_cls
from .rans_model import rans_model as rans_model_cls
class viscous(Group):
    """
    'viscous' child.
    """

    fluent_name = "viscous"

    child_names = \
        ['model', 'options', 'spalart_allmaras_production', 'k_epsilon_model',
         'k_omega_model', 'k_omega_options', 'rng_options',
         'near_wall_treatment', 'transition_sst_options',
         'reynolds_stress_model', 'subgrid_scale_model', 'les_model_options',
         'reynolds_stress_options', 'enhanced_wall_treatment_options',
         'rans_model']

    model: model_cls = model_cls
    """
    model child of viscous.
    """
    options: options_cls = options_cls
    """
    options child of viscous.
    """
    spalart_allmaras_production: spalart_allmaras_production_cls = spalart_allmaras_production_cls
    """
    spalart_allmaras_production child of viscous.
    """
    k_epsilon_model: k_epsilon_model_cls = k_epsilon_model_cls
    """
    k_epsilon_model child of viscous.
    """
    k_omega_model: k_omega_model_cls = k_omega_model_cls
    """
    k_omega_model child of viscous.
    """
    k_omega_options: k_omega_options_cls = k_omega_options_cls
    """
    k_omega_options child of viscous.
    """
    rng_options: rng_options_cls = rng_options_cls
    """
    rng_options child of viscous.
    """
    near_wall_treatment: near_wall_treatment_cls = near_wall_treatment_cls
    """
    near_wall_treatment child of viscous.
    """
    transition_sst_options: transition_sst_options_cls = transition_sst_options_cls
    """
    transition_sst_options child of viscous.
    """
    reynolds_stress_model: reynolds_stress_model_cls = reynolds_stress_model_cls
    """
    reynolds_stress_model child of viscous.
    """
    subgrid_scale_model: subgrid_scale_model_cls = subgrid_scale_model_cls
    """
    subgrid_scale_model child of viscous.
    """
    les_model_options: les_model_options_cls = les_model_options_cls
    """
    les_model_options child of viscous.
    """
    reynolds_stress_options: reynolds_stress_options_cls = reynolds_stress_options_cls
    """
    reynolds_stress_options child of viscous.
    """
    enhanced_wall_treatment_options: enhanced_wall_treatment_options_cls = enhanced_wall_treatment_options_cls
    """
    enhanced_wall_treatment_options child of viscous.
    """
    rans_model: rans_model_cls = rans_model_cls
    """
    rans_model child of viscous.
    """
