#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .background import background as background_cls
from .color_by_type import color_by_type as color_by_type_cls
from .foreground import foreground as foreground_cls
from .by_type import by_type as by_type_cls
from .by_surface import by_surface as by_surface_cls
from .far_field_faces import far_field_faces as far_field_faces_cls
from .inlet_faces import inlet_faces as inlet_faces_cls
from .interior_faces import interior_faces as interior_faces_cls
from .internal_faces import internal_faces as internal_faces_cls
from .outlet_faces import outlet_faces as outlet_faces_cls
from .overset_faces import overset_faces as overset_faces_cls
from .periodic_faces import periodic_faces as periodic_faces_cls
from .rans_les_interface_faces import rans_les_interface_faces as rans_les_interface_faces_cls
from .symmetry_faces import symmetry_faces as symmetry_faces_cls
from .axis_faces import axis_faces as axis_faces_cls
from .free_surface_faces import free_surface_faces as free_surface_faces_cls
from .traction_faces import traction_faces as traction_faces_cls
from .wall_faces import wall_faces as wall_faces_cls
from .interface_faces import interface_faces as interface_faces_cls
from .surface_3 import surface as surface_cls
from .skip_label import skip_label as skip_label_cls
from .automatic_skip import automatic_skip as automatic_skip_cls
from .reset_colors import reset_colors as reset_colors_cls
from .list_colors import list_colors as list_colors_cls
class colors(Group):
    """
    'colors' child.
    """

    fluent_name = "colors"

    child_names = \
        ['background', 'color_by_type', 'foreground', 'by_type', 'by_surface',
         'far_field_faces', 'inlet_faces', 'interior_faces', 'internal_faces',
         'outlet_faces', 'overset_faces', 'periodic_faces',
         'rans_les_interface_faces', 'symmetry_faces', 'axis_faces',
         'free_surface_faces', 'traction_faces', 'wall_faces',
         'interface_faces', 'surface', 'skip_label', 'automatic_skip']

    background: background_cls = background_cls
    """
    background child of colors.
    """
    color_by_type: color_by_type_cls = color_by_type_cls
    """
    color_by_type child of colors.
    """
    foreground: foreground_cls = foreground_cls
    """
    foreground child of colors.
    """
    by_type: by_type_cls = by_type_cls
    """
    by_type child of colors.
    """
    by_surface: by_surface_cls = by_surface_cls
    """
    by_surface child of colors.
    """
    far_field_faces: far_field_faces_cls = far_field_faces_cls
    """
    far_field_faces child of colors.
    """
    inlet_faces: inlet_faces_cls = inlet_faces_cls
    """
    inlet_faces child of colors.
    """
    interior_faces: interior_faces_cls = interior_faces_cls
    """
    interior_faces child of colors.
    """
    internal_faces: internal_faces_cls = internal_faces_cls
    """
    internal_faces child of colors.
    """
    outlet_faces: outlet_faces_cls = outlet_faces_cls
    """
    outlet_faces child of colors.
    """
    overset_faces: overset_faces_cls = overset_faces_cls
    """
    overset_faces child of colors.
    """
    periodic_faces: periodic_faces_cls = periodic_faces_cls
    """
    periodic_faces child of colors.
    """
    rans_les_interface_faces: rans_les_interface_faces_cls = rans_les_interface_faces_cls
    """
    rans_les_interface_faces child of colors.
    """
    symmetry_faces: symmetry_faces_cls = symmetry_faces_cls
    """
    symmetry_faces child of colors.
    """
    axis_faces: axis_faces_cls = axis_faces_cls
    """
    axis_faces child of colors.
    """
    free_surface_faces: free_surface_faces_cls = free_surface_faces_cls
    """
    free_surface_faces child of colors.
    """
    traction_faces: traction_faces_cls = traction_faces_cls
    """
    traction_faces child of colors.
    """
    wall_faces: wall_faces_cls = wall_faces_cls
    """
    wall_faces child of colors.
    """
    interface_faces: interface_faces_cls = interface_faces_cls
    """
    interface_faces child of colors.
    """
    surface: surface_cls = surface_cls
    """
    surface child of colors.
    """
    skip_label: skip_label_cls = skip_label_cls
    """
    skip_label child of colors.
    """
    automatic_skip: automatic_skip_cls = automatic_skip_cls
    """
    automatic_skip child of colors.
    """
    command_names = \
        ['reset_colors', 'list_colors']

    reset_colors: reset_colors_cls = reset_colors_cls
    """
    reset_colors command of colors.
    """
    list_colors: list_colors_cls = list_colors_cls
    """
    list_colors command of colors.
    """
