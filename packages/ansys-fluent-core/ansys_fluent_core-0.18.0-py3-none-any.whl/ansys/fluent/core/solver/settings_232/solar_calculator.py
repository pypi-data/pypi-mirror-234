#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .latitude import latitude as latitude_cls
from .longitude import longitude as longitude_cls
from .timezone import timezone as timezone_cls
from .north_direction import north_direction as north_direction_cls
from .east_direction import east_direction as east_direction_cls
from .date_and_time import date_and_time as date_and_time_cls
from .calculator_method import calculator_method as calculator_method_cls
from .sunshine_factor import sunshine_factor as sunshine_factor_cls
class solar_calculator(Group):
    """
    'solar_calculator' child.
    """

    fluent_name = "solar-calculator"

    child_names = \
        ['latitude', 'longitude', 'timezone', 'north_direction',
         'east_direction', 'date_and_time', 'calculator_method',
         'sunshine_factor']

    latitude: latitude_cls = latitude_cls
    """
    latitude child of solar_calculator.
    """
    longitude: longitude_cls = longitude_cls
    """
    longitude child of solar_calculator.
    """
    timezone: timezone_cls = timezone_cls
    """
    timezone child of solar_calculator.
    """
    north_direction: north_direction_cls = north_direction_cls
    """
    north_direction child of solar_calculator.
    """
    east_direction: east_direction_cls = east_direction_cls
    """
    east_direction child of solar_calculator.
    """
    date_and_time: date_and_time_cls = date_and_time_cls
    """
    date_and_time child of solar_calculator.
    """
    calculator_method: calculator_method_cls = calculator_method_cls
    """
    calculator_method child of solar_calculator.
    """
    sunshine_factor: sunshine_factor_cls = sunshine_factor_cls
    """
    sunshine_factor child of solar_calculator.
    """
