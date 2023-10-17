#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .viewfactor_settings import viewfactor_settings as viewfactor_settings_cls
from .clustering_settings import clustering_settings as clustering_settings_cls
from .radiosity_solver_control import radiosity_solver_control as radiosity_solver_control_cls
from .compute_write_vf import compute_write_vf as compute_write_vf_cls
from .compute_vf_accelerated import compute_vf_accelerated as compute_vf_accelerated_cls
from .compute_clusters_and_vf_accelerated import compute_clusters_and_vf_accelerated as compute_clusters_and_vf_accelerated_cls
from .compute_vf_only import compute_vf_only as compute_vf_only_cls
from .read_vf_file import read_vf_file as read_vf_file_cls
class s2s(Group):
    """
    's2s' child.
    """

    fluent_name = "s2s"

    child_names = \
        ['viewfactor_settings', 'clustering_settings',
         'radiosity_solver_control']

    viewfactor_settings: viewfactor_settings_cls = viewfactor_settings_cls
    """
    viewfactor_settings child of s2s.
    """
    clustering_settings: clustering_settings_cls = clustering_settings_cls
    """
    clustering_settings child of s2s.
    """
    radiosity_solver_control: radiosity_solver_control_cls = radiosity_solver_control_cls
    """
    radiosity_solver_control child of s2s.
    """
    command_names = \
        ['compute_write_vf', 'compute_vf_accelerated',
         'compute_clusters_and_vf_accelerated', 'compute_vf_only',
         'read_vf_file']

    compute_write_vf: compute_write_vf_cls = compute_write_vf_cls
    """
    compute_write_vf command of s2s.
    """
    compute_vf_accelerated: compute_vf_accelerated_cls = compute_vf_accelerated_cls
    """
    compute_vf_accelerated command of s2s.
    """
    compute_clusters_and_vf_accelerated: compute_clusters_and_vf_accelerated_cls = compute_clusters_and_vf_accelerated_cls
    """
    compute_clusters_and_vf_accelerated command of s2s.
    """
    compute_vf_only: compute_vf_only_cls = compute_vf_only_cls
    """
    compute_vf_only command of s2s.
    """
    read_vf_file: read_vf_file_cls = read_vf_file_cls
    """
    read_vf_file command of s2s.
    """
