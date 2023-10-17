#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fluid_1 import fluid as fluid_cls
from .solid_1 import solid as solid_cls
from .copy_1 import copy as copy_cls
from .change_type import change_type as change_type_cls
from .activate_cell_zone import activate_cell_zone as activate_cell_zone_cls
from .mrf_to_sliding_mesh import mrf_to_sliding_mesh as mrf_to_sliding_mesh_cls
from .convert_all_solid_mrf_to_solid_motion import convert_all_solid_mrf_to_solid_motion as convert_all_solid_mrf_to_solid_motion_cls
from .copy_mrf_to_mesh_motion import copy_mrf_to_mesh_motion as copy_mrf_to_mesh_motion_cls
from .copy_mesh_to_mrf_motion import copy_mesh_to_mrf_motion as copy_mesh_to_mrf_motion_cls
class cell_zone_conditions(Group, _ChildNamedObjectAccessorMixin):
    """
    'cell_zone_conditions' child.
    """

    fluent_name = "cell-zone-conditions"

    child_names = \
        ['fluid', 'solid']

    fluid: fluid_cls = fluid_cls
    """
    fluid child of cell_zone_conditions.
    """
    solid: solid_cls = solid_cls
    """
    solid child of cell_zone_conditions.
    """
    command_names = \
        ['copy', 'change_type', 'activate_cell_zone', 'mrf_to_sliding_mesh',
         'convert_all_solid_mrf_to_solid_motion', 'copy_mrf_to_mesh_motion',
         'copy_mesh_to_mrf_motion']

    copy: copy_cls = copy_cls
    """
    copy command of cell_zone_conditions.
    """
    change_type: change_type_cls = change_type_cls
    """
    change_type command of cell_zone_conditions.
    """
    activate_cell_zone: activate_cell_zone_cls = activate_cell_zone_cls
    """
    activate_cell_zone command of cell_zone_conditions.
    """
    mrf_to_sliding_mesh: mrf_to_sliding_mesh_cls = mrf_to_sliding_mesh_cls
    """
    mrf_to_sliding_mesh command of cell_zone_conditions.
    """
    convert_all_solid_mrf_to_solid_motion: convert_all_solid_mrf_to_solid_motion_cls = convert_all_solid_mrf_to_solid_motion_cls
    """
    convert_all_solid_mrf_to_solid_motion command of cell_zone_conditions.
    """
    copy_mrf_to_mesh_motion: copy_mrf_to_mesh_motion_cls = copy_mrf_to_mesh_motion_cls
    """
    copy_mrf_to_mesh_motion command of cell_zone_conditions.
    """
    copy_mesh_to_mrf_motion: copy_mesh_to_mrf_motion_cls = copy_mesh_to_mrf_motion_cls
    """
    copy_mesh_to_mrf_motion command of cell_zone_conditions.
    """
