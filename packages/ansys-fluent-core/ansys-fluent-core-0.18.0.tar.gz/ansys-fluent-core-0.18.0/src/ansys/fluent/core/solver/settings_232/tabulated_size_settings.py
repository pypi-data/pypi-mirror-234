#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .table_name import table_name as table_name_cls
from .column_with_diameters import column_with_diameters as column_with_diameters_cls
from .column_with_number_fractions import column_with_number_fractions as column_with_number_fractions_cls
from .column_with_mass_fractions import column_with_mass_fractions as column_with_mass_fractions_cls
from .accumulated_number_fraction import accumulated_number_fraction as accumulated_number_fraction_cls
from .accumulated_mass_fraction import accumulated_mass_fraction as accumulated_mass_fraction_cls
class tabulated_size_settings(Group):
    """
    'tabulated_size_settings' child.
    """

    fluent_name = "tabulated-size-settings"

    child_names = \
        ['table_name', 'column_with_diameters',
         'column_with_number_fractions', 'column_with_mass_fractions',
         'accumulated_number_fraction', 'accumulated_mass_fraction']

    table_name: table_name_cls = table_name_cls
    """
    table_name child of tabulated_size_settings.
    """
    column_with_diameters: column_with_diameters_cls = column_with_diameters_cls
    """
    column_with_diameters child of tabulated_size_settings.
    """
    column_with_number_fractions: column_with_number_fractions_cls = column_with_number_fractions_cls
    """
    column_with_number_fractions child of tabulated_size_settings.
    """
    column_with_mass_fractions: column_with_mass_fractions_cls = column_with_mass_fractions_cls
    """
    column_with_mass_fractions child of tabulated_size_settings.
    """
    accumulated_number_fraction: accumulated_number_fraction_cls = accumulated_number_fraction_cls
    """
    accumulated_number_fraction child of tabulated_size_settings.
    """
    accumulated_mass_fraction: accumulated_mass_fraction_cls = accumulated_mass_fraction_cls
    """
    accumulated_mass_fraction child of tabulated_size_settings.
    """
