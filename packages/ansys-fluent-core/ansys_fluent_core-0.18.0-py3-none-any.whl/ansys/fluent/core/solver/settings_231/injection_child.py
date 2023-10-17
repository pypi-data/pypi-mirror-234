#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_type import report_type as report_type_cls
from .user_specified_origin_and_axis import user_specified_origin_and_axis as user_specified_origin_and_axis_cls
from .origin_1 import origin as origin_cls
from .axis_1 import axis as axis_cls
from .mass_criterion import mass_criterion as mass_criterion_cls
from .physics import physics as physics_cls
from .boundary_zones_names import boundary_zones_names as boundary_zones_names_cls
from .boundary_zones_1 import boundary_zones as boundary_zones_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .inj_mass_rate_last_tstp import inj_mass_rate_last_tstp as inj_mass_rate_last_tstp_cls
from .inj_mass_rate_last_flow import inj_mass_rate_last_flow as inj_mass_rate_last_flow_cls
from .inj_mass_rate_prev_mass import inj_mass_rate_prev_mass as inj_mass_rate_prev_mass_cls
from .inj_mass_rate_prev_time import inj_mass_rate_prev_time as inj_mass_rate_prev_time_cls
from .show_unsteady_rate import show_unsteady_rate as show_unsteady_rate_cls
from .old_props import old_props as old_props_cls
from .average_over import average_over as average_over_cls
from .per_injection import per_injection as per_injection_cls
from .injection_list import injection_list as injection_list_cls
class injection_child(Group):
    """
    'child_object_type' of injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'user_specified_origin_and_axis', 'origin', 'axis',
         'mass_criterion', 'physics', 'boundary_zones_names',
         'boundary_zones', 'retain_instantaneous_values',
         'inj_mass_rate_last_tstp', 'inj_mass_rate_last_flow',
         'inj_mass_rate_prev_mass', 'inj_mass_rate_prev_time',
         'show_unsteady_rate', 'old_props', 'average_over', 'per_injection',
         'injection_list']

    report_type: report_type_cls = report_type_cls
    """
    report_type child of injection_child.
    """
    user_specified_origin_and_axis: user_specified_origin_and_axis_cls = user_specified_origin_and_axis_cls
    """
    user_specified_origin_and_axis child of injection_child.
    """
    origin: origin_cls = origin_cls
    """
    origin child of injection_child.
    """
    axis: axis_cls = axis_cls
    """
    axis child of injection_child.
    """
    mass_criterion: mass_criterion_cls = mass_criterion_cls
    """
    mass_criterion child of injection_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of injection_child.
    """
    boundary_zones_names: boundary_zones_names_cls = boundary_zones_names_cls
    """
    boundary_zones_names child of injection_child.
    """
    boundary_zones: boundary_zones_cls = boundary_zones_cls
    """
    boundary_zones child of injection_child.
    """
    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of injection_child.
    """
    inj_mass_rate_last_tstp: inj_mass_rate_last_tstp_cls = inj_mass_rate_last_tstp_cls
    """
    inj_mass_rate_last_tstp child of injection_child.
    """
    inj_mass_rate_last_flow: inj_mass_rate_last_flow_cls = inj_mass_rate_last_flow_cls
    """
    inj_mass_rate_last_flow child of injection_child.
    """
    inj_mass_rate_prev_mass: inj_mass_rate_prev_mass_cls = inj_mass_rate_prev_mass_cls
    """
    inj_mass_rate_prev_mass child of injection_child.
    """
    inj_mass_rate_prev_time: inj_mass_rate_prev_time_cls = inj_mass_rate_prev_time_cls
    """
    inj_mass_rate_prev_time child of injection_child.
    """
    show_unsteady_rate: show_unsteady_rate_cls = show_unsteady_rate_cls
    """
    show_unsteady_rate child of injection_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of injection_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of injection_child.
    """
    per_injection: per_injection_cls = per_injection_cls
    """
    per_injection child of injection_child.
    """
    injection_list: injection_list_cls = injection_list_cls
    """
    injection_list child of injection_child.
    """
