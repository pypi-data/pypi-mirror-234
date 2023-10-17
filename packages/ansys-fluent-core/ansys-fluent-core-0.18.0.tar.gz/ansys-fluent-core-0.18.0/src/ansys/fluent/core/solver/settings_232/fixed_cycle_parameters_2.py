#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pre_sweeps_3 import pre_sweeps as pre_sweeps_cls
from .post_sweeps_2 import post_sweeps as post_sweeps_cls
class fixed_cycle_parameters(Group):
    """
    'fixed_cycle_parameters' child.
    """

    fluent_name = "fixed-cycle-parameters"

    child_names = \
        ['pre_sweeps', 'post_sweeps']

    pre_sweeps: pre_sweeps_cls = pre_sweeps_cls
    """
    pre_sweeps child of fixed_cycle_parameters.
    """
    post_sweeps: post_sweeps_cls = post_sweeps_cls
    """
    post_sweeps child of fixed_cycle_parameters.
    """
