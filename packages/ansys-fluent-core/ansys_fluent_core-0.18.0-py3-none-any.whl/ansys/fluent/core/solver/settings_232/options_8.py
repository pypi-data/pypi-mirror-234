#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .nodes import nodes as nodes_cls
from .edges_1 import edges as edges_cls
from .faces_1 import faces as faces_cls
from .partitions import partitions as partitions_cls
from .overset_2 import overset as overset_cls
from .gap import gap as gap_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['nodes', 'edges', 'faces', 'partitions', 'overset', 'gap']

    nodes: nodes_cls = nodes_cls
    """
    nodes child of options.
    """
    edges: edges_cls = edges_cls
    """
    edges child of options.
    """
    faces: faces_cls = faces_cls
    """
    faces child of options.
    """
    partitions: partitions_cls = partitions_cls
    """
    partitions child of options.
    """
    overset: overset_cls = overset_cls
    """
    overset child of options.
    """
    gap: gap_cls = gap_cls
    """
    gap child of options.
    """
