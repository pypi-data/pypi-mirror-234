#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model_2 import model as model_cls
from .options_3 import options as options_cls
from .reactions import reactions as reactions_cls
from .wall_surface_options import wall_surface_options as wall_surface_options_cls
from .turb_chem_interaction_model import turb_chem_interaction_model as turb_chem_interaction_model_cls
from .turb_chem_interaction_model_options import turb_chem_interaction_model_options as turb_chem_interaction_model_options_cls
from .species_transport_expert_options import species_transport_expert_options as species_transport_expert_options_cls
from .edc_model_options import edc_model_options as edc_model_options_cls
from .tfm_model_options import tfm_model_options as tfm_model_options_cls
from .chemistry_solver import chemistry_solver as chemistry_solver_cls
from .integration_parameters import integration_parameters as integration_parameters_cls
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['model', 'options', 'reactions', 'wall_surface_options',
         'turb_chem_interaction_model', 'turb_chem_interaction_model_options',
         'species_transport_expert_options', 'edc_model_options',
         'tfm_model_options', 'chemistry_solver', 'integration_parameters']

    model: model_cls = model_cls
    """
    model child of species.
    """
    options: options_cls = options_cls
    """
    options child of species.
    """
    reactions: reactions_cls = reactions_cls
    """
    reactions child of species.
    """
    wall_surface_options: wall_surface_options_cls = wall_surface_options_cls
    """
    wall_surface_options child of species.
    """
    turb_chem_interaction_model: turb_chem_interaction_model_cls = turb_chem_interaction_model_cls
    """
    turb_chem_interaction_model child of species.
    """
    turb_chem_interaction_model_options: turb_chem_interaction_model_options_cls = turb_chem_interaction_model_options_cls
    """
    turb_chem_interaction_model_options child of species.
    """
    species_transport_expert_options: species_transport_expert_options_cls = species_transport_expert_options_cls
    """
    species_transport_expert_options child of species.
    """
    edc_model_options: edc_model_options_cls = edc_model_options_cls
    """
    edc_model_options child of species.
    """
    tfm_model_options: tfm_model_options_cls = tfm_model_options_cls
    """
    tfm_model_options child of species.
    """
    chemistry_solver: chemistry_solver_cls = chemistry_solver_cls
    """
    chemistry_solver child of species.
    """
    integration_parameters: integration_parameters_cls = integration_parameters_cls
    """
    integration_parameters child of species.
    """
