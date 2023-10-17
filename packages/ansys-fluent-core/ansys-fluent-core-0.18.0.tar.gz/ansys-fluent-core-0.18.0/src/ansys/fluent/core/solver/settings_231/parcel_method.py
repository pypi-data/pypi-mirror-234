#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .const_number_in_parcel import const_number_in_parcel as const_number_in_parcel_cls
from .const_parcel_mass import const_parcel_mass as const_parcel_mass_cls
from .const_parcel_diameter import const_parcel_diameter as const_parcel_diameter_cls
class parcel_method(Group):
    """
    'parcel_method' child.
    """

    fluent_name = "parcel-method"

    child_names = \
        ['option', 'const_number_in_parcel', 'const_parcel_mass',
         'const_parcel_diameter']

    option: option_cls = option_cls
    """
    option child of parcel_method.
    """
    const_number_in_parcel: const_number_in_parcel_cls = const_number_in_parcel_cls
    """
    const_number_in_parcel child of parcel_method.
    """
    const_parcel_mass: const_parcel_mass_cls = const_parcel_mass_cls
    """
    const_parcel_mass child of parcel_method.
    """
    const_parcel_diameter: const_parcel_diameter_cls = const_parcel_diameter_cls
    """
    const_parcel_diameter child of parcel_method.
    """
