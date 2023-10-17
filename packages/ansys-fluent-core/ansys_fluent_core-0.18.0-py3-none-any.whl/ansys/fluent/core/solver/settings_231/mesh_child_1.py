#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .options_5 import options as options_cls
from .edge_type import edge_type as edge_type_cls
from .shrink_factor import shrink_factor as shrink_factor_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .coloring_1 import coloring as coloring_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_3 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_2 import display as display_cls
class mesh_child(Group):
    """
    'child_object_type' of mesh.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'options', 'edge_type', 'shrink_factor', 'surfaces_list',
         'coloring', 'display_state_name', 'physics', 'geometry', 'surfaces']

    name: name_cls = name_cls
    """
    name child of mesh_child.
    """
    options: options_cls = options_cls
    """
    options child of mesh_child.
    """
    edge_type: edge_type_cls = edge_type_cls
    """
    edge_type child of mesh_child.
    """
    shrink_factor: shrink_factor_cls = shrink_factor_cls
    """
    shrink_factor child of mesh_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of mesh_child.
    """
    coloring: coloring_cls = coloring_cls
    """
    coloring child of mesh_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of mesh_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of mesh_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of mesh_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of mesh_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of mesh_child.
    """
