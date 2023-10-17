#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .scaled import scaled as scaled_cls
from .report_type import report_type as report_type_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .thread_names import thread_names as thread_names_cls
from .thread_ids import thread_ids as thread_ids_cls
from .old_props import old_props as old_props_cls
from .reference_frame import reference_frame as reference_frame_cls
from .mom_axis import mom_axis as mom_axis_cls
from .mom_center import mom_center as mom_center_cls
class moment_child(Group):
    """
    'child_object_type' of moment.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'scaled', 'report_type',
         'average_over', 'per_zone', 'thread_names', 'thread_ids',
         'old_props', 'reference_frame', 'mom_axis', 'mom_center']

    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of moment_child.
    """
    scaled: scaled_cls = scaled_cls
    """
    scaled child of moment_child.
    """
    report_type: report_type_cls = report_type_cls
    """
    report_type child of moment_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of moment_child.
    """
    per_zone: per_zone_cls = per_zone_cls
    """
    per_zone child of moment_child.
    """
    thread_names: thread_names_cls = thread_names_cls
    """
    thread_names child of moment_child.
    """
    thread_ids: thread_ids_cls = thread_ids_cls
    """
    thread_ids child of moment_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of moment_child.
    """
    reference_frame: reference_frame_cls = reference_frame_cls
    """
    reference_frame child of moment_child.
    """
    mom_axis: mom_axis_cls = mom_axis_cls
    """
    mom_axis child of moment_child.
    """
    mom_center: mom_center_cls = mom_center_cls
    """
    mom_center child of moment_child.
    """
