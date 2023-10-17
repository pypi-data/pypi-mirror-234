#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pre_sweeps_2 import pre_sweeps as pre_sweeps_cls
from .post_sweeps_1 import post_sweeps as post_sweeps_cls
from .max_cycle_1 import max_cycle as max_cycle_cls
class fixed_cycle_parameters(Group):
    """
    'fixed_cycle_parameters' child.
    """

    fluent_name = "fixed-cycle-parameters"

    child_names = \
        ['pre_sweeps', 'post_sweeps', 'max_cycle']

    pre_sweeps: pre_sweeps_cls = pre_sweeps_cls
    """
    pre_sweeps child of fixed_cycle_parameters.
    """
    post_sweeps: post_sweeps_cls = post_sweeps_cls
    """
    post_sweeps child of fixed_cycle_parameters.
    """
    max_cycle: max_cycle_cls = max_cycle_cls
    """
    max_cycle child of fixed_cycle_parameters.
    """
