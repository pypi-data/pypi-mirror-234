#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .smoothing_iteration import smoothing_iteration as smoothing_iteration_cls
class smooth_partition(Command):
    """
    Smooth partition interface.
    
    Parameters
    ----------
        smoothing_iteration : int
            Set maximum number of smoothing iterations.
    
    """

    fluent_name = "smooth-partition"

    argument_names = \
        ['smoothing_iteration']

    smoothing_iteration: smoothing_iteration_cls = smoothing_iteration_cls
    """
    smoothing_iteration argument of smooth_partition.
    """
