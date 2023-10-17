#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_inherent_material_color_1 import use_inherent_material_color as use_inherent_material_color_cls
from .reset import reset as reset_cls
from .list_surfaces_by_color import list_surfaces_by_color as list_surfaces_by_color_cls
from .list_surfaces_by_material import list_surfaces_by_material as list_surfaces_by_material_cls
class by_surface(Group):
    """
    'by_surface' child.
    """

    fluent_name = "by-surface"

    child_names = \
        ['use_inherent_material_color']

    use_inherent_material_color: use_inherent_material_color_cls = use_inherent_material_color_cls
    """
    use_inherent_material_color child of by_surface.
    """
    command_names = \
        ['reset', 'list_surfaces_by_color', 'list_surfaces_by_material']

    reset: reset_cls = reset_cls
    """
    reset command of by_surface.
    """
    list_surfaces_by_color: list_surfaces_by_color_cls = list_surfaces_by_color_cls
    """
    list_surfaces_by_color command of by_surface.
    """
    list_surfaces_by_material: list_surfaces_by_material_cls = list_surfaces_by_material_cls
    """
    list_surfaces_by_material command of by_surface.
    """
