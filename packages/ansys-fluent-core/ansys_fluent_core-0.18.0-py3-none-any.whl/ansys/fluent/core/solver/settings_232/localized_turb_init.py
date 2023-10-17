#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_3 import enabled as enabled_cls
from .turbulent_intensity import turbulent_intensity as turbulent_intensity_cls
from .turbulent_viscosity_ratio import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
class localized_turb_init(Group):
    """
    Localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models.
    """

    fluent_name = "localized-turb-init"

    child_names = \
        ['enabled', 'turbulent_intensity', 'turbulent_viscosity_ratio']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of localized_turb_init.
    """
    turbulent_intensity: turbulent_intensity_cls = turbulent_intensity_cls
    """
    turbulent_intensity child of localized_turb_init.
    """
    turbulent_viscosity_ratio: turbulent_viscosity_ratio_cls = turbulent_viscosity_ratio_cls
    """
    turbulent_viscosity_ratio child of localized_turb_init.
    """
