#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_mesh_interface_clustering import enable_mesh_interface_clustering as enable_mesh_interface_clustering_cls
from .split_angle import split_angle as split_angle_cls
from .clustering_algorithm import clustering_algorithm as clustering_algorithm_cls
from .faces_per_cluster import faces_per_cluster as faces_per_cluster_cls
from .print_thread_clusters import print_thread_clusters as print_thread_clusters_cls
class clustering_settings(Group):
    """
    Enter clustering related settings.
    """

    fluent_name = "clustering-settings"

    child_names = \
        ['enable_mesh_interface_clustering', 'split_angle',
         'clustering_algorithm', 'faces_per_cluster']

    enable_mesh_interface_clustering: enable_mesh_interface_clustering_cls = enable_mesh_interface_clustering_cls
    """
    enable_mesh_interface_clustering child of clustering_settings.
    """
    split_angle: split_angle_cls = split_angle_cls
    """
    split_angle child of clustering_settings.
    """
    clustering_algorithm: clustering_algorithm_cls = clustering_algorithm_cls
    """
    clustering_algorithm child of clustering_settings.
    """
    faces_per_cluster: faces_per_cluster_cls = faces_per_cluster_cls
    """
    faces_per_cluster child of clustering_settings.
    """
    command_names = \
        ['print_thread_clusters']

    print_thread_clusters: print_thread_clusters_cls = print_thread_clusters_cls
    """
    print_thread_clusters command of clustering_settings.
    """
