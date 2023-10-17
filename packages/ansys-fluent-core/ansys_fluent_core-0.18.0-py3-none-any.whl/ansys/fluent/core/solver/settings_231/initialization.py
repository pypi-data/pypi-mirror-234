#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fmg_initialize import fmg_initialize as fmg_initialize_cls
from .localized_turb_init import localized_turb_init as localized_turb_init_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .fmg_options import fmg_options as fmg_options_cls
from .hybrid_init_options import hybrid_init_options as hybrid_init_options_cls
from .patch import patch as patch_cls
from .set_defaults import set_defaults as set_defaults_cls
from .open_channel_auto_init import open_channel_auto_init as open_channel_auto_init_cls
from .fmg_initialization import fmg_initialization as fmg_initialization_cls
from .initialization_type import initialization_type as initialization_type_cls
from .standard_initialize import standard_initialize as standard_initialize_cls
from .hybrid_initialize import hybrid_initialize as hybrid_initialize_cls
from .initialize import initialize as initialize_cls
from .dpm_reset import dpm_reset as dpm_reset_cls
from .lwf_reset import lwf_reset as lwf_reset_cls
from .init_flow_statistics import init_flow_statistics as init_flow_statistics_cls
from .init_acoustics_options import init_acoustics_options as init_acoustics_options_cls
from .list_defaults import list_defaults as list_defaults_cls
from .init_turb_vel_fluctuations import init_turb_vel_fluctuations as init_turb_vel_fluctuations_cls
from .show_iterations_sampled import show_iterations_sampled as show_iterations_sampled_cls
from .show_time_sampled import show_time_sampled as show_time_sampled_cls
from .levelset_auto_init import levelset_auto_init as levelset_auto_init_cls
class initialization(Group):
    """
    'initialization' child.
    """

    fluent_name = "initialization"

    child_names = \
        ['fmg_initialize', 'localized_turb_init', 'reference_frame',
         'fmg_options', 'hybrid_init_options', 'patch', 'set_defaults',
         'open_channel_auto_init', 'fmg_initialization',
         'initialization_type']

    fmg_initialize: fmg_initialize_cls = fmg_initialize_cls
    """
    fmg_initialize child of initialization.
    """
    localized_turb_init: localized_turb_init_cls = localized_turb_init_cls
    """
    localized_turb_init child of initialization.
    """
    reference_frame: reference_frame_cls = reference_frame_cls
    """
    reference_frame child of initialization.
    """
    fmg_options: fmg_options_cls = fmg_options_cls
    """
    fmg_options child of initialization.
    """
    hybrid_init_options: hybrid_init_options_cls = hybrid_init_options_cls
    """
    hybrid_init_options child of initialization.
    """
    patch: patch_cls = patch_cls
    """
    patch child of initialization.
    """
    set_defaults: set_defaults_cls = set_defaults_cls
    """
    set_defaults child of initialization.
    """
    open_channel_auto_init: open_channel_auto_init_cls = open_channel_auto_init_cls
    """
    open_channel_auto_init child of initialization.
    """
    fmg_initialization: fmg_initialization_cls = fmg_initialization_cls
    """
    fmg_initialization child of initialization.
    """
    initialization_type: initialization_type_cls = initialization_type_cls
    """
    initialization_type child of initialization.
    """
    command_names = \
        ['standard_initialize', 'hybrid_initialize', 'initialize',
         'dpm_reset', 'lwf_reset', 'init_flow_statistics',
         'init_acoustics_options', 'list_defaults',
         'init_turb_vel_fluctuations', 'show_iterations_sampled',
         'show_time_sampled', 'levelset_auto_init']

    standard_initialize: standard_initialize_cls = standard_initialize_cls
    """
    standard_initialize command of initialization.
    """
    hybrid_initialize: hybrid_initialize_cls = hybrid_initialize_cls
    """
    hybrid_initialize command of initialization.
    """
    initialize: initialize_cls = initialize_cls
    """
    initialize command of initialization.
    """
    dpm_reset: dpm_reset_cls = dpm_reset_cls
    """
    dpm_reset command of initialization.
    """
    lwf_reset: lwf_reset_cls = lwf_reset_cls
    """
    lwf_reset command of initialization.
    """
    init_flow_statistics: init_flow_statistics_cls = init_flow_statistics_cls
    """
    init_flow_statistics command of initialization.
    """
    init_acoustics_options: init_acoustics_options_cls = init_acoustics_options_cls
    """
    init_acoustics_options command of initialization.
    """
    list_defaults: list_defaults_cls = list_defaults_cls
    """
    list_defaults command of initialization.
    """
    init_turb_vel_fluctuations: init_turb_vel_fluctuations_cls = init_turb_vel_fluctuations_cls
    """
    init_turb_vel_fluctuations command of initialization.
    """
    show_iterations_sampled: show_iterations_sampled_cls = show_iterations_sampled_cls
    """
    show_iterations_sampled command of initialization.
    """
    show_time_sampled: show_time_sampled_cls = show_time_sampled_cls
    """
    show_time_sampled command of initialization.
    """
    levelset_auto_init: levelset_auto_init_cls = levelset_auto_init_cls
    """
    levelset_auto_init command of initialization.
    """
