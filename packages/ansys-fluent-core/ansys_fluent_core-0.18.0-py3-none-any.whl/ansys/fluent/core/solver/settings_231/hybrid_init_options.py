#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .general_settings_1 import general_settings as general_settings_cls
from .turbulent_setting import turbulent_setting as turbulent_setting_cls
from .species_setting import species_setting as species_setting_cls
class hybrid_init_options(Group):
    """
    Enter the settings for hybrid initialization method.
    """

    fluent_name = "hybrid-init-options"

    child_names = \
        ['general_settings', 'turbulent_setting', 'species_setting']

    general_settings: general_settings_cls = general_settings_cls
    """
    general_settings child of hybrid_init_options.
    """
    turbulent_setting: turbulent_setting_cls = turbulent_setting_cls
    """
    turbulent_setting child of hybrid_init_options.
    """
    species_setting: species_setting_cls = species_setting_cls
    """
    species_setting child of hybrid_init_options.
    """
