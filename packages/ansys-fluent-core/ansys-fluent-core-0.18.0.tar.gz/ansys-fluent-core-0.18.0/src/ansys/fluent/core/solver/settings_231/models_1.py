#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .discrete_phase import discrete_phase as discrete_phase_cls
from .energy import energy as energy_cls
from .multiphase import multiphase as multiphase_cls
from .viscous import viscous as viscous_cls
from .optics import optics as optics_cls
from .virtual_blade_model import virtual_blade_model as virtual_blade_model_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['discrete_phase', 'energy', 'multiphase', 'viscous', 'optics',
         'virtual_blade_model']

    discrete_phase: discrete_phase_cls = discrete_phase_cls
    """
    discrete_phase child of models.
    """
    energy: energy_cls = energy_cls
    """
    energy child of models.
    """
    multiphase: multiphase_cls = multiphase_cls
    """
    multiphase child of models.
    """
    viscous: viscous_cls = viscous_cls
    """
    viscous child of models.
    """
    optics: optics_cls = optics_cls
    """
    optics child of models.
    """
    virtual_blade_model: virtual_blade_model_cls = virtual_blade_model_cls
    """
    virtual_blade_model child of models.
    """
