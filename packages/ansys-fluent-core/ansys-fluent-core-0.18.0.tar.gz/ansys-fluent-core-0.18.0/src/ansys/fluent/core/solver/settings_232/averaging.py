#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .node_based_averaging_enabled import node_based_averaging_enabled as node_based_averaging_enabled_cls
from .source_term_averaging_enabled import source_term_averaging_enabled as source_term_averaging_enabled_cls
from .averaging_every_step_enabled import averaging_every_step_enabled as averaging_every_step_enabled_cls
from .averaging_kernel import averaging_kernel as averaging_kernel_cls
class averaging(Group):
    """
    Menu containing options to enable/disable node-based averaging of DPM variables and DPM source terms. 
    Please note that node-based averaging functionality is only available if source term linearization is not active.
    """

    fluent_name = "averaging"

    child_names = \
        ['node_based_averaging_enabled', 'source_term_averaging_enabled',
         'averaging_every_step_enabled', 'averaging_kernel']

    node_based_averaging_enabled: node_based_averaging_enabled_cls = node_based_averaging_enabled_cls
    """
    node_based_averaging_enabled child of averaging.
    """
    source_term_averaging_enabled: source_term_averaging_enabled_cls = source_term_averaging_enabled_cls
    """
    source_term_averaging_enabled child of averaging.
    """
    averaging_every_step_enabled: averaging_every_step_enabled_cls = averaging_every_step_enabled_cls
    """
    averaging_every_step_enabled child of averaging.
    """
    averaging_kernel: averaging_kernel_cls = averaging_kernel_cls
    """
    averaging_kernel child of averaging.
    """
