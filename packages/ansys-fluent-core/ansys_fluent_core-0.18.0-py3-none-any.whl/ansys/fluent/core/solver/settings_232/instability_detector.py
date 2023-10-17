#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_instability_detector import enable_instability_detector as enable_instability_detector_cls
from .set_cfl_limit import set_cfl_limit as set_cfl_limit_cls
from .set_cfl_type import set_cfl_type as set_cfl_type_cls
from .set_velocity_limit import set_velocity_limit as set_velocity_limit_cls
from .unstable_event_outer_iterations import unstable_event_outer_iterations as unstable_event_outer_iterations_cls
class instability_detector(Group):
    """
    Set Hybrid NITA instability detector controls.
    """

    fluent_name = "instability-detector"

    child_names = \
        ['enable_instability_detector', 'set_cfl_limit', 'set_cfl_type',
         'set_velocity_limit', 'unstable_event_outer_iterations']

    enable_instability_detector: enable_instability_detector_cls = enable_instability_detector_cls
    """
    enable_instability_detector child of instability_detector.
    """
    set_cfl_limit: set_cfl_limit_cls = set_cfl_limit_cls
    """
    set_cfl_limit child of instability_detector.
    """
    set_cfl_type: set_cfl_type_cls = set_cfl_type_cls
    """
    set_cfl_type child of instability_detector.
    """
    set_velocity_limit: set_velocity_limit_cls = set_velocity_limit_cls
    """
    set_velocity_limit child of instability_detector.
    """
    unstable_event_outer_iterations: unstable_event_outer_iterations_cls = unstable_event_outer_iterations_cls
    """
    unstable_event_outer_iterations child of instability_detector.
    """
