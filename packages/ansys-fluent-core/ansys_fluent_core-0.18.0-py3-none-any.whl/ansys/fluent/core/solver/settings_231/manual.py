#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .faces_1 import faces as faces_cls
from .edges_1 import edges as edges_cls
from .nodes_1 import nodes as nodes_cls
from .material_color import material_color as material_color_cls
class manual(Group):
    """
    'manual' child.
    """

    fluent_name = "manual"

    child_names = \
        ['faces', 'edges', 'nodes', 'material_color']

    faces: faces_cls = faces_cls
    """
    faces child of manual.
    """
    edges: edges_cls = edges_cls
    """
    edges child of manual.
    """
    nodes: nodes_cls = nodes_cls
    """
    nodes child of manual.
    """
    material_color: material_color_cls = material_color_cls
    """
    material_color child of manual.
    """
