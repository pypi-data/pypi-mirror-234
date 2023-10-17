#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .multiphase import multiphase as multiphase_cls
from .energy import energy as energy_cls
from .viscous import viscous as viscous_cls
from .radiation import radiation as radiation_cls
from .species import species as species_cls
from .discrete_phase import discrete_phase as discrete_phase_cls
from .virtual_blade_model import virtual_blade_model as virtual_blade_model_cls
from .optics import optics as optics_cls
from .structure import structure as structure_cls
from .ablation import ablation as ablation_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['multiphase', 'energy', 'viscous', 'radiation', 'species',
         'discrete_phase', 'virtual_blade_model', 'optics', 'structure',
         'ablation']

    multiphase: multiphase_cls = multiphase_cls
    """
    multiphase child of models.
    """
    energy: energy_cls = energy_cls
    """
    energy child of models.
    """
    viscous: viscous_cls = viscous_cls
    """
    viscous child of models.
    """
    radiation: radiation_cls = radiation_cls
    """
    radiation child of models.
    """
    species: species_cls = species_cls
    """
    species child of models.
    """
    discrete_phase: discrete_phase_cls = discrete_phase_cls
    """
    discrete_phase child of models.
    """
    virtual_blade_model: virtual_blade_model_cls = virtual_blade_model_cls
    """
    virtual_blade_model child of models.
    """
    optics: optics_cls = optics_cls
    """
    optics child of models.
    """
    structure: structure_cls = structure_cls
    """
    structure child of models.
    """
    ablation: ablation_cls = ablation_cls
    """
    ablation child of models.
    """
