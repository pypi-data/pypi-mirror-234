#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .reference_pressure import reference_pressure as reference_pressure_cls
from .reference_density import reference_density as reference_density_cls
from .reference_bulk_modulus import reference_bulk_modulus as reference_bulk_modulus_cls
from .density_exponent import density_exponent as density_exponent_cls
from .maximum_density_ratio import maximum_density_ratio as maximum_density_ratio_cls
from .minimum_density_ratio import minimum_density_ratio as minimum_density_ratio_cls
class compressible_liquid(Group):
    """
    'compressible_liquid' child.
    """

    fluent_name = "compressible-liquid"

    child_names = \
        ['reference_pressure', 'reference_density', 'reference_bulk_modulus',
         'density_exponent', 'maximum_density_ratio',
         'minimum_density_ratio']

    reference_pressure: reference_pressure_cls = reference_pressure_cls
    """
    reference_pressure child of compressible_liquid.
    """
    reference_density: reference_density_cls = reference_density_cls
    """
    reference_density child of compressible_liquid.
    """
    reference_bulk_modulus: reference_bulk_modulus_cls = reference_bulk_modulus_cls
    """
    reference_bulk_modulus child of compressible_liquid.
    """
    density_exponent: density_exponent_cls = density_exponent_cls
    """
    density_exponent child of compressible_liquid.
    """
    maximum_density_ratio: maximum_density_ratio_cls = maximum_density_ratio_cls
    """
    maximum_density_ratio child of compressible_liquid.
    """
    minimum_density_ratio: minimum_density_ratio_cls = minimum_density_ratio_cls
    """
    minimum_density_ratio child of compressible_liquid.
    """
