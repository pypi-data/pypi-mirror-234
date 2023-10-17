#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_high_res_tracking import enable_high_res_tracking as enable_high_res_tracking_cls
from .expert_options_1 import expert_options as expert_options_cls
from .high_res_tracking_options import high_res_tracking_options as high_res_tracking_options_cls
from .tracking_parameters import tracking_parameters as tracking_parameters_cls
from .track_in_absolute_frame import track_in_absolute_frame as track_in_absolute_frame_cls
class tracking(Group):
    """
    Main menu to control the time integration of the particle trajectory equations.
    """

    fluent_name = "tracking"

    child_names = \
        ['enable_high_res_tracking', 'expert_options',
         'high_res_tracking_options', 'tracking_parameters',
         'track_in_absolute_frame']

    enable_high_res_tracking: enable_high_res_tracking_cls = enable_high_res_tracking_cls
    """
    enable_high_res_tracking child of tracking.
    """
    expert_options: expert_options_cls = expert_options_cls
    """
    expert_options child of tracking.
    """
    high_res_tracking_options: high_res_tracking_options_cls = high_res_tracking_options_cls
    """
    high_res_tracking_options child of tracking.
    """
    tracking_parameters: tracking_parameters_cls = tracking_parameters_cls
    """
    tracking_parameters child of tracking.
    """
    track_in_absolute_frame: track_in_absolute_frame_cls = track_in_absolute_frame_cls
    """
    track_in_absolute_frame child of tracking.
    """
