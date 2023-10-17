#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .options_1 import options as options_cls
from .convert_domain import convert_domain as convert_domain_cls
from .convert_hanging_nodes import convert_hanging_nodes as convert_hanging_nodes_cls
from .convert_hanging_node_zones import convert_hanging_node_zones as convert_hanging_node_zones_cls
from .convert_skewed_cells_1 import convert_skewed_cells as convert_skewed_cells_cls
class polyhedra(Group):
    """
    Enter the polyhedra menu.
    """

    fluent_name = "polyhedra"

    child_names = \
        ['options']

    options: options_cls = options_cls
    """
    options child of polyhedra.
    """
    command_names = \
        ['convert_domain', 'convert_hanging_nodes',
         'convert_hanging_node_zones', 'convert_skewed_cells']

    convert_domain: convert_domain_cls = convert_domain_cls
    """
    convert_domain command of polyhedra.
    """
    convert_hanging_nodes: convert_hanging_nodes_cls = convert_hanging_nodes_cls
    """
    convert_hanging_nodes command of polyhedra.
    """
    convert_hanging_node_zones: convert_hanging_node_zones_cls = convert_hanging_node_zones_cls
    """
    convert_hanging_node_zones command of polyhedra.
    """
    convert_skewed_cells: convert_skewed_cells_cls = convert_skewed_cells_cls
    """
    convert_skewed_cells command of polyhedra.
    """
