#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_1 import phase as phase_cls
from .name_1 import name as name_cls
from .material import material as material_cls
from .sources import sources as sources_cls
from .source_terms_1 import source_terms as source_terms_cls
from .fixed import fixed as fixed_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .fixes import fixes as fixes_cls
from .motion_spec import motion_spec as motion_spec_cls
from .relative_to_thread import relative_to_thread as relative_to_thread_cls
from .omega import omega as omega_cls
from .axis_origin_1 import axis_origin as axis_origin_cls
from .axis_direction_1 import axis_direction as axis_direction_cls
from .udf_zmotion_name import udf_zmotion_name as udf_zmotion_name_cls
from .mrf_motion import mrf_motion as mrf_motion_cls
from .mrf_relative_to_thread import mrf_relative_to_thread as mrf_relative_to_thread_cls
from .mrf_omega import mrf_omega as mrf_omega_cls
from .reference_frame_velocity import reference_frame_velocity as reference_frame_velocity_cls
from .reference_frame_axis_origin import reference_frame_axis_origin as reference_frame_axis_origin_cls
from .reference_frame_axis_direction import reference_frame_axis_direction as reference_frame_axis_direction_cls
from .mrf_udf_zmotion_name import mrf_udf_zmotion_name as mrf_udf_zmotion_name_cls
from .mgrid_enable_transient import mgrid_enable_transient as mgrid_enable_transient_cls
from .mgrid_motion import mgrid_motion as mgrid_motion_cls
from .mgrid_relative_to_thread import mgrid_relative_to_thread as mgrid_relative_to_thread_cls
from .mgrid_omega import mgrid_omega as mgrid_omega_cls
from .moving_mesh_velocity import moving_mesh_velocity as moving_mesh_velocity_cls
from .moving_mesh_axis_origin import moving_mesh_axis_origin as moving_mesh_axis_origin_cls
from .moving_mesh_axis_direction import moving_mesh_axis_direction as moving_mesh_axis_direction_cls
from .mgrid_udf_zmotion_name import mgrid_udf_zmotion_name as mgrid_udf_zmotion_name_cls
from .solid_motion import solid_motion as solid_motion_cls
from .solid_relative_to_thread import solid_relative_to_thread as solid_relative_to_thread_cls
from .solid_omega import solid_omega as solid_omega_cls
from .solid_motion_velocity import solid_motion_velocity as solid_motion_velocity_cls
from .solid_motion_axis_origin import solid_motion_axis_origin as solid_motion_axis_origin_cls
from .solid_motion_axis_direction import solid_motion_axis_direction as solid_motion_axis_direction_cls
from .solid_udf_zmotion_name import solid_udf_zmotion_name as solid_udf_zmotion_name_cls
from .radiating import radiating as radiating_cls
from .les_embedded import les_embedded as les_embedded_cls
from .contact_property import contact_property as contact_property_cls
from .active_wetsteam_zone import active_wetsteam_zone as active_wetsteam_zone_cls
from .vapor_phase_realgas import vapor_phase_realgas as vapor_phase_realgas_cls
from .cursys import cursys as cursys_cls
from .cursys_name import cursys_name as cursys_name_cls
from .pcb_model import pcb_model as pcb_model_cls
from .pcb_zone_info import pcb_zone_info as pcb_zone_info_cls
class solid_child(Group):
    """
    'child_object_type' of solid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'name', 'material', 'sources', 'source_terms', 'fixed',
         'cylindrical_fixed_var', 'fixes', 'motion_spec',
         'relative_to_thread', 'omega', 'axis_origin', 'axis_direction',
         'udf_zmotion_name', 'mrf_motion', 'mrf_relative_to_thread',
         'mrf_omega', 'reference_frame_velocity',
         'reference_frame_axis_origin', 'reference_frame_axis_direction',
         'mrf_udf_zmotion_name', 'mgrid_enable_transient', 'mgrid_motion',
         'mgrid_relative_to_thread', 'mgrid_omega', 'moving_mesh_velocity',
         'moving_mesh_axis_origin', 'moving_mesh_axis_direction',
         'mgrid_udf_zmotion_name', 'solid_motion', 'solid_relative_to_thread',
         'solid_omega', 'solid_motion_velocity', 'solid_motion_axis_origin',
         'solid_motion_axis_direction', 'solid_udf_zmotion_name', 'radiating',
         'les_embedded', 'contact_property', 'active_wetsteam_zone',
         'vapor_phase_realgas', 'cursys', 'cursys_name', 'pcb_model',
         'pcb_zone_info']

    phase: phase_cls = phase_cls
    """
    phase child of solid_child.
    """
    name: name_cls = name_cls
    """
    name child of solid_child.
    """
    material: material_cls = material_cls
    """
    material child of solid_child.
    """
    sources: sources_cls = sources_cls
    """
    sources child of solid_child.
    """
    source_terms: source_terms_cls = source_terms_cls
    """
    source_terms child of solid_child.
    """
    fixed: fixed_cls = fixed_cls
    """
    fixed child of solid_child.
    """
    cylindrical_fixed_var: cylindrical_fixed_var_cls = cylindrical_fixed_var_cls
    """
    cylindrical_fixed_var child of solid_child.
    """
    fixes: fixes_cls = fixes_cls
    """
    fixes child of solid_child.
    """
    motion_spec: motion_spec_cls = motion_spec_cls
    """
    motion_spec child of solid_child.
    """
    relative_to_thread: relative_to_thread_cls = relative_to_thread_cls
    """
    relative_to_thread child of solid_child.
    """
    omega: omega_cls = omega_cls
    """
    omega child of solid_child.
    """
    axis_origin: axis_origin_cls = axis_origin_cls
    """
    axis_origin child of solid_child.
    """
    axis_direction: axis_direction_cls = axis_direction_cls
    """
    axis_direction child of solid_child.
    """
    udf_zmotion_name: udf_zmotion_name_cls = udf_zmotion_name_cls
    """
    udf_zmotion_name child of solid_child.
    """
    mrf_motion: mrf_motion_cls = mrf_motion_cls
    """
    mrf_motion child of solid_child.
    """
    mrf_relative_to_thread: mrf_relative_to_thread_cls = mrf_relative_to_thread_cls
    """
    mrf_relative_to_thread child of solid_child.
    """
    mrf_omega: mrf_omega_cls = mrf_omega_cls
    """
    mrf_omega child of solid_child.
    """
    reference_frame_velocity: reference_frame_velocity_cls = reference_frame_velocity_cls
    """
    reference_frame_velocity child of solid_child.
    """
    reference_frame_axis_origin: reference_frame_axis_origin_cls = reference_frame_axis_origin_cls
    """
    reference_frame_axis_origin child of solid_child.
    """
    reference_frame_axis_direction: reference_frame_axis_direction_cls = reference_frame_axis_direction_cls
    """
    reference_frame_axis_direction child of solid_child.
    """
    mrf_udf_zmotion_name: mrf_udf_zmotion_name_cls = mrf_udf_zmotion_name_cls
    """
    mrf_udf_zmotion_name child of solid_child.
    """
    mgrid_enable_transient: mgrid_enable_transient_cls = mgrid_enable_transient_cls
    """
    mgrid_enable_transient child of solid_child.
    """
    mgrid_motion: mgrid_motion_cls = mgrid_motion_cls
    """
    mgrid_motion child of solid_child.
    """
    mgrid_relative_to_thread: mgrid_relative_to_thread_cls = mgrid_relative_to_thread_cls
    """
    mgrid_relative_to_thread child of solid_child.
    """
    mgrid_omega: mgrid_omega_cls = mgrid_omega_cls
    """
    mgrid_omega child of solid_child.
    """
    moving_mesh_velocity: moving_mesh_velocity_cls = moving_mesh_velocity_cls
    """
    moving_mesh_velocity child of solid_child.
    """
    moving_mesh_axis_origin: moving_mesh_axis_origin_cls = moving_mesh_axis_origin_cls
    """
    moving_mesh_axis_origin child of solid_child.
    """
    moving_mesh_axis_direction: moving_mesh_axis_direction_cls = moving_mesh_axis_direction_cls
    """
    moving_mesh_axis_direction child of solid_child.
    """
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name_cls = mgrid_udf_zmotion_name_cls
    """
    mgrid_udf_zmotion_name child of solid_child.
    """
    solid_motion: solid_motion_cls = solid_motion_cls
    """
    solid_motion child of solid_child.
    """
    solid_relative_to_thread: solid_relative_to_thread_cls = solid_relative_to_thread_cls
    """
    solid_relative_to_thread child of solid_child.
    """
    solid_omega: solid_omega_cls = solid_omega_cls
    """
    solid_omega child of solid_child.
    """
    solid_motion_velocity: solid_motion_velocity_cls = solid_motion_velocity_cls
    """
    solid_motion_velocity child of solid_child.
    """
    solid_motion_axis_origin: solid_motion_axis_origin_cls = solid_motion_axis_origin_cls
    """
    solid_motion_axis_origin child of solid_child.
    """
    solid_motion_axis_direction: solid_motion_axis_direction_cls = solid_motion_axis_direction_cls
    """
    solid_motion_axis_direction child of solid_child.
    """
    solid_udf_zmotion_name: solid_udf_zmotion_name_cls = solid_udf_zmotion_name_cls
    """
    solid_udf_zmotion_name child of solid_child.
    """
    radiating: radiating_cls = radiating_cls
    """
    radiating child of solid_child.
    """
    les_embedded: les_embedded_cls = les_embedded_cls
    """
    les_embedded child of solid_child.
    """
    contact_property: contact_property_cls = contact_property_cls
    """
    contact_property child of solid_child.
    """
    active_wetsteam_zone: active_wetsteam_zone_cls = active_wetsteam_zone_cls
    """
    active_wetsteam_zone child of solid_child.
    """
    vapor_phase_realgas: vapor_phase_realgas_cls = vapor_phase_realgas_cls
    """
    vapor_phase_realgas child of solid_child.
    """
    cursys: cursys_cls = cursys_cls
    """
    cursys child of solid_child.
    """
    cursys_name: cursys_name_cls = cursys_name_cls
    """
    cursys_name child of solid_child.
    """
    pcb_model: pcb_model_cls = pcb_model_cls
    """
    pcb_model child of solid_child.
    """
    pcb_zone_info: pcb_zone_info_cls = pcb_zone_info_cls
    """
    pcb_zone_info child of solid_child.
    """
