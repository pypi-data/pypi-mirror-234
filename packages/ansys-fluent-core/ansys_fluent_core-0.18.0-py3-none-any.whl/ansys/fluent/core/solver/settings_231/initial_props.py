#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .location import location as location_cls
from .matrix import matrix as matrix_cls
from .cone_settings import cone_settings as cone_settings_cls
from .velocity import velocity as velocity_cls
from .angular_velocity import angular_velocity as angular_velocity_cls
from .flow_rate_1 import flow_rate as flow_rate_cls
from .times import times as times_cls
from .diameter_1 import diameter as diameter_cls
from .temperature import temperature as temperature_cls
from .temperature_2 import temperature_2 as temperature_2_cls
class initial_props(Group):
    """
    'initial_props' child.
    """

    fluent_name = "initial-props"

    child_names = \
        ['location', 'matrix', 'cone_settings', 'velocity',
         'angular_velocity', 'flow_rate', 'times', 'diameter', 'temperature',
         'temperature_2']

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
    flow_rate: flow_rate_cls = flow_rate_cls
    """
    flow_rate child of initial_props.
    """
    times: times_cls = times_cls
    """
    times child of initial_props.
    """
    diameter: diameter_cls = diameter_cls
    """
    diameter child of initial_props.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of initial_props.
    """
    temperature_2: temperature_2_cls = temperature_2_cls
    """
    temperature_2 child of initial_props.
    """
