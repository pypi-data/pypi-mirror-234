#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solar_frequency_data import solar_frequency_data as solar_frequency_data_cls
from .solar_filename import solar_filename as solar_filename_cls
from .use_binary_format import use_binary_format as use_binary_format_cls
class autosave_solar_data(Group):
    """
    'autosave_solar_data' child.
    """

    fluent_name = "autosave-solar-data"

    child_names = \
        ['solar_frequency_data', 'solar_filename', 'use_binary_format']

    solar_frequency_data: solar_frequency_data_cls = solar_frequency_data_cls
    """
    solar_frequency_data child of autosave_solar_data.
    """
    solar_filename: solar_filename_cls = solar_filename_cls
    """
    solar_filename child of autosave_solar_data.
    """
    use_binary_format: use_binary_format_cls = use_binary_format_cls
    """
    use_binary_format child of autosave_solar_data.
    """
