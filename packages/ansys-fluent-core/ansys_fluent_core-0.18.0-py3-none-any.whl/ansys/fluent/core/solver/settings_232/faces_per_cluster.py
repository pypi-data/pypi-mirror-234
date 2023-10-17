#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_1 import option as option_cls
from .global_faces_per_surface_cluster import global_faces_per_surface_cluster as global_faces_per_surface_cluster_cls
from .maximum_faces_per_surface_cluster import maximum_faces_per_surface_cluster as maximum_faces_per_surface_cluster_cls
class faces_per_cluster(Group):
    """
    'faces_per_cluster' child.
    """

    fluent_name = "faces-per-cluster"

    child_names = \
        ['option', 'global_faces_per_surface_cluster',
         'maximum_faces_per_surface_cluster']

    option: option_cls = option_cls
    """
    option child of faces_per_cluster.
    """
    global_faces_per_surface_cluster: global_faces_per_surface_cluster_cls = global_faces_per_surface_cluster_cls
    """
    global_faces_per_surface_cluster child of faces_per_cluster.
    """
    maximum_faces_per_surface_cluster: maximum_faces_per_surface_cluster_cls = maximum_faces_per_surface_cluster_cls
    """
    maximum_faces_per_surface_cluster child of faces_per_cluster.
    """
