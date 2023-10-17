#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .in_plane import in_plane as in_plane_cls
from .fixed_length import fixed_length as fixed_length_cls
from .x_comp import x_comp as x_comp_cls
from .y_comp import y_comp as y_comp_cls
from .z_comp import z_comp as z_comp_cls
from .scale_head import scale_head as scale_head_cls
from .color import color as color_cls
class vector_opt(Group):
    """
    'vector_opt' child.
    """

    fluent_name = "vector-opt"

    child_names = \
        ['in_plane', 'fixed_length', 'x_comp', 'y_comp', 'z_comp',
         'scale_head', 'color']

    in_plane: in_plane_cls = in_plane_cls
    """
    in_plane child of vector_opt.
    """
    fixed_length: fixed_length_cls = fixed_length_cls
    """
    fixed_length child of vector_opt.
    """
    x_comp: x_comp_cls = x_comp_cls
    """
    x_comp child of vector_opt.
    """
    y_comp: y_comp_cls = y_comp_cls
    """
    y_comp child of vector_opt.
    """
    z_comp: z_comp_cls = z_comp_cls
    """
    z_comp child of vector_opt.
    """
    scale_head: scale_head_cls = scale_head_cls
    """
    scale_head child of vector_opt.
    """
    color: color_cls = color_cls
    """
    color child of vector_opt.
    """
