#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .direct_solar_irradiation import direct_solar_irradiation as direct_solar_irradiation_cls
from .diffuse_solar_irradiation import diffuse_solar_irradiation as diffuse_solar_irradiation_cls
from .spectral_fraction import spectral_fraction as spectral_fraction_cls
class illumination_parameters(Group):
    """
    'illumination_parameters' child.
    """

    fluent_name = "illumination-parameters"

    child_names = \
        ['direct_solar_irradiation', 'diffuse_solar_irradiation',
         'spectral_fraction']

    direct_solar_irradiation: direct_solar_irradiation_cls = direct_solar_irradiation_cls
    """
    direct_solar_irradiation child of illumination_parameters.
    """
    diffuse_solar_irradiation: diffuse_solar_irradiation_cls = diffuse_solar_irradiation_cls
    """
    diffuse_solar_irradiation child of illumination_parameters.
    """
    spectral_fraction: spectral_fraction_cls = spectral_fraction_cls
    """
    spectral_fraction child of illumination_parameters.
    """
