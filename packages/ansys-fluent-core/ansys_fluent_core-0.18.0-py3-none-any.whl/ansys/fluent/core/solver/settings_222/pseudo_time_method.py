#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .formulation import formulation as formulation_cls
from .local_time_step_settings import local_time_step_settings as local_time_step_settings_cls
from .global_time_step_settings import global_time_step_settings as global_time_step_settings_cls
from .advanced_options import advanced_options as advanced_options_cls
from .relaxation_factors import relaxation_factors as relaxation_factors_cls
from .verbosity_3 import verbosity as verbosity_cls
class pseudo_time_method(Group):
    """
    'pseudo_time_method' child.
    """

    fluent_name = "pseudo-time-method"

    child_names = \
        ['formulation', 'local_time_step_settings',
         'global_time_step_settings', 'advanced_options',
         'relaxation_factors', 'verbosity']

    formulation: formulation_cls = formulation_cls
    """
    formulation child of pseudo_time_method.
    """
    local_time_step_settings: local_time_step_settings_cls = local_time_step_settings_cls
    """
    local_time_step_settings child of pseudo_time_method.
    """
    global_time_step_settings: global_time_step_settings_cls = global_time_step_settings_cls
    """
    global_time_step_settings child of pseudo_time_method.
    """
    advanced_options: advanced_options_cls = advanced_options_cls
    """
    advanced_options child of pseudo_time_method.
    """
    relaxation_factors: relaxation_factors_cls = relaxation_factors_cls
    """
    relaxation_factors child of pseudo_time_method.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of pseudo_time_method.
    """
