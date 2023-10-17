#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .particle_drag import particle_drag as particle_drag_cls
from .particle_rotation import particle_rotation as particle_rotation_cls
from .heat_transfer import heat_transfer as heat_transfer_cls
from .custom_laws import custom_laws as custom_laws_cls
from .turbulent_dispersion import turbulent_dispersion as turbulent_dispersion_cls
from .droplet_breakup import droplet_breakup as droplet_breakup_cls
class physical_models(Group):
    """
    'physical_models' child.
    """

    fluent_name = "physical-models"

    child_names = \
        ['particle_drag', 'particle_rotation', 'heat_transfer', 'custom_laws',
         'turbulent_dispersion', 'droplet_breakup']

    particle_drag: particle_drag_cls = particle_drag_cls
    """
    particle_drag child of physical_models.
    """
    particle_rotation: particle_rotation_cls = particle_rotation_cls
    """
    particle_rotation child of physical_models.
    """
    heat_transfer: heat_transfer_cls = heat_transfer_cls
    """
    heat_transfer child of physical_models.
    """
    custom_laws: custom_laws_cls = custom_laws_cls
    """
    custom_laws child of physical_models.
    """
    turbulent_dispersion: turbulent_dispersion_cls = turbulent_dispersion_cls
    """
    turbulent_dispersion child of physical_models.
    """
    droplet_breakup: droplet_breakup_cls = droplet_breakup_cls
    """
    droplet_breakup child of physical_models.
    """
