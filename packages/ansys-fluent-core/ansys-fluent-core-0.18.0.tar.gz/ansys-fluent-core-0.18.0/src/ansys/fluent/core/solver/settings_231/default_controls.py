#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .recommended_defaults_for_existing_cases import recommended_defaults_for_existing_cases as recommended_defaults_for_existing_cases_cls
from .revert_to_pre_r20_1_default_settings import revert_to_pre_r20_1_default_settings as revert_to_pre_r20_1_default_settings_cls
class default_controls(Group):
    """
    Multiphase default controls menu.
    """

    fluent_name = "default-controls"

    child_names = \
        ['recommended_defaults_for_existing_cases',
         'revert_to_pre_r20_1_default_settings']

    recommended_defaults_for_existing_cases: recommended_defaults_for_existing_cases_cls = recommended_defaults_for_existing_cases_cls
    """
    recommended_defaults_for_existing_cases child of default_controls.
    """
    revert_to_pre_r20_1_default_settings: revert_to_pre_r20_1_default_settings_cls = revert_to_pre_r20_1_default_settings_cls
    """
    revert_to_pre_r20_1_default_settings child of default_controls.
    """
