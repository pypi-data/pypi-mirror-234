#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .merge_iterations import merge_iterations as merge_iterations_cls
class merge_clusters(Command):
    """
    Merge partition clusters.
    
    Parameters
    ----------
        merge_iterations : int
            'merge_iterations' child.
    
    """

    fluent_name = "merge-clusters"

    argument_names = \
        ['merge_iterations']

    merge_iterations: merge_iterations_cls = merge_iterations_cls
    """
    merge_iterations argument of merge_clusters.
    """
