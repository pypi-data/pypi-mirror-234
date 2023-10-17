#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .location_1 import location as location_cls
from .matrix import matrix as matrix_cls
from .cone_settings import cone_settings as cone_settings_cls
from .velocity import velocity as velocity_cls
from .angular_velocity import angular_velocity as angular_velocity_cls
from .mass_flow_rate import mass_flow_rate as mass_flow_rate_cls
from .times import times as times_cls
from .particle_size import particle_size as particle_size_cls
from .temperature import temperature as temperature_cls
from .temperature_2 import temperature_2 as temperature_2_cls
class initial_props(Group):
    """
    'initial_props' child.
    """

    fluent_name = "initial-props"

    child_names = \
        ['location', 'matrix', 'cone_settings', 'velocity',
         'angular_velocity', 'mass_flow_rate', 'times', 'particle_size',
         'temperature', 'temperature_2']

    location: location_cls = location_cls
    """
    location child of initial_props.
    """
    matrix: matrix_cls = matrix_cls
    """
    matrix child of initial_props.
    """
    cone_settings: cone_settings_cls = cone_settings_cls
    """
    cone_settings child of initial_props.
    """
    velocity: velocity_cls = velocity_cls
    """
    velocity child of initial_props.
    """
    angular_velocity: angular_velocity_cls = angular_velocity_cls
    """
    angular_velocity child of initial_props.
    """
    mass_flow_rate: mass_flow_rate_cls = mass_flow_rate_cls
    """
    mass_flow_rate child of initial_props.
    """
    times: times_cls = times_cls
    """
    times child of initial_props.
    """
    particle_size: particle_size_cls = particle_size_cls
    """
    particle_size child of initial_props.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of initial_props.
    """
    temperature_2: temperature_2_cls = temperature_2_cls
    """
    temperature_2 child of initial_props.
    """
