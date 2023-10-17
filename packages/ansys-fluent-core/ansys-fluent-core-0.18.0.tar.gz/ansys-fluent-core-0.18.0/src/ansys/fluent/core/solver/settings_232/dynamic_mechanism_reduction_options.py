#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .dynamic_mechanism_reduction_tolerance import dynamic_mechanism_reduction_tolerance as dynamic_mechanism_reduction_tolerance_cls
from .dynamic_mechanism_reduction_expert import dynamic_mechanism_reduction_expert as dynamic_mechanism_reduction_expert_cls
from .dynamic_mechanism_reduction_min_target import dynamic_mechanism_reduction_min_target as dynamic_mechanism_reduction_min_target_cls
from .dynamic_mechanism_reduction_target_threshold import dynamic_mechanism_reduction_target_threshold as dynamic_mechanism_reduction_target_threshold_cls
from .dynamic_mechanism_reduction_targets import dynamic_mechanism_reduction_targets as dynamic_mechanism_reduction_targets_cls
class dynamic_mechanism_reduction_options(Group):
    """
    'dynamic_mechanism_reduction_options' child.
    """

    fluent_name = "dynamic-mechanism-reduction-options"

    child_names = \
        ['dynamic_mechanism_reduction_tolerance',
         'dynamic_mechanism_reduction_expert',
         'dynamic_mechanism_reduction_min_target',
         'dynamic_mechanism_reduction_target_threshold',
         'dynamic_mechanism_reduction_targets']

    dynamic_mechanism_reduction_tolerance: dynamic_mechanism_reduction_tolerance_cls = dynamic_mechanism_reduction_tolerance_cls
    """
    dynamic_mechanism_reduction_tolerance child of dynamic_mechanism_reduction_options.
    """
    dynamic_mechanism_reduction_expert: dynamic_mechanism_reduction_expert_cls = dynamic_mechanism_reduction_expert_cls
    """
    dynamic_mechanism_reduction_expert child of dynamic_mechanism_reduction_options.
    """
    dynamic_mechanism_reduction_min_target: dynamic_mechanism_reduction_min_target_cls = dynamic_mechanism_reduction_min_target_cls
    """
    dynamic_mechanism_reduction_min_target child of dynamic_mechanism_reduction_options.
    """
    dynamic_mechanism_reduction_target_threshold: dynamic_mechanism_reduction_target_threshold_cls = dynamic_mechanism_reduction_target_threshold_cls
    """
    dynamic_mechanism_reduction_target_threshold child of dynamic_mechanism_reduction_options.
    """
    dynamic_mechanism_reduction_targets: dynamic_mechanism_reduction_targets_cls = dynamic_mechanism_reduction_targets_cls
    """
    dynamic_mechanism_reduction_targets child of dynamic_mechanism_reduction_options.
    """
