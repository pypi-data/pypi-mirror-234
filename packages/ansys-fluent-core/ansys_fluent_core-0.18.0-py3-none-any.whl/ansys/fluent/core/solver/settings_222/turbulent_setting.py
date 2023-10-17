#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .averaged_turbulent_parameters import averaged_turbulent_parameters as averaged_turbulent_parameters_cls
from .turbulent_intensity_1 import turbulent_intensity as turbulent_intensity_cls
from .viscosity_ratio_1 import viscosity_ratio as viscosity_ratio_cls
class turbulent_setting(Group):
    """
    Enter the turbulent settings menu.
    """

    fluent_name = "turbulent-setting"

    child_names = \
        ['averaged_turbulent_parameters', 'turbulent_intensity',
         'viscosity_ratio']

    averaged_turbulent_parameters: averaged_turbulent_parameters_cls = averaged_turbulent_parameters_cls
    """
    averaged_turbulent_parameters child of turbulent_setting.
    """
    turbulent_intensity: turbulent_intensity_cls = turbulent_intensity_cls
    """
    turbulent_intensity child of turbulent_setting.
    """
    viscosity_ratio: viscosity_ratio_cls = viscosity_ratio_cls
    """
    viscosity_ratio child of turbulent_setting.
    """
