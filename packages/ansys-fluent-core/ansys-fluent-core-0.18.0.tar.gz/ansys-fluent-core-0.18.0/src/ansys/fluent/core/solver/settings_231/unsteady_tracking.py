#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_1 import option as option_cls
from .create_particles_every_particle_step import create_particles_every_particle_step as create_particles_every_particle_step_cls
from .dpm_time_step import dpm_time_step as dpm_time_step_cls
from .n_time_steps import n_time_steps as n_time_steps_cls
from .clear_particles_from_domain import clear_particles_from_domain as clear_particles_from_domain_cls
class unsteady_tracking(Group):
    """
    'unsteady_tracking' child.
    """

    fluent_name = "unsteady-tracking"

    child_names = \
        ['option', 'create_particles_every_particle_step', 'dpm_time_step',
         'n_time_steps', 'clear_particles_from_domain']

    option: option_cls = option_cls
    """
    option child of unsteady_tracking.
    """
    create_particles_every_particle_step: create_particles_every_particle_step_cls = create_particles_every_particle_step_cls
    """
    create_particles_every_particle_step child of unsteady_tracking.
    """
    dpm_time_step: dpm_time_step_cls = dpm_time_step_cls
    """
    dpm_time_step child of unsteady_tracking.
    """
    n_time_steps: n_time_steps_cls = n_time_steps_cls
    """
    n_time_steps child of unsteady_tracking.
    """
    clear_particles_from_domain: clear_particles_from_domain_cls = clear_particles_from_domain_cls
    """
    clear_particles_from_domain child of unsteady_tracking.
    """
