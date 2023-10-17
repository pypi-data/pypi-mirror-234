#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .hexahedron import hexahedron as hexahedron_cls
from .sphere import sphere as sphere_cls
from .cylinder import cylinder as cylinder_cls
from .boundary import boundary as boundary_cls
from .limiters import limiters as limiters_cls
from .field_value import field_value as field_value_cls
from .residual import residual as residual_cls
from .volume_1 import volume as volume_cls
from .yplus_star import yplus_star as yplus_star_cls
from .yplus_ystar import yplus_ystar as yplus_ystar_cls
class type(Group):
    """
    'type' child.
    """

    fluent_name = "type"

    child_names = \
        ['option', 'hexahedron', 'sphere', 'cylinder', 'boundary', 'limiters',
         'field_value', 'residual', 'volume', 'yplus_star', 'yplus_ystar']

    option: option_cls = option_cls
    """
    option child of type.
    """
    hexahedron: hexahedron_cls = hexahedron_cls
    """
    hexahedron child of type.
    """
    sphere: sphere_cls = sphere_cls
    """
    sphere child of type.
    """
    cylinder: cylinder_cls = cylinder_cls
    """
    cylinder child of type.
    """
    boundary: boundary_cls = boundary_cls
    """
    boundary child of type.
    """
    limiters: limiters_cls = limiters_cls
    """
    limiters child of type.
    """
    field_value: field_value_cls = field_value_cls
    """
    field_value child of type.
    """
    residual: residual_cls = residual_cls
    """
    residual child of type.
    """
    volume: volume_cls = volume_cls
    """
    volume child of type.
    """
    yplus_star: yplus_star_cls = yplus_star_cls
    """
    yplus_star child of type.
    """
    yplus_ystar: yplus_ystar_cls = yplus_ystar_cls
    """
    yplus_ystar child of type.
    """
