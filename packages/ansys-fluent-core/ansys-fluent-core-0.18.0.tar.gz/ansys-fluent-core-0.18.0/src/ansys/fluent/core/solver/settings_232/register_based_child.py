#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_2 import name as name_cls
from .register import register as register_cls
from .frequency_2 import frequency as frequency_cls
from .active_1 import active as active_cls
from .verbosity_9 import verbosity as verbosity_cls
from .monitor_1 import monitor as monitor_cls
class register_based_child(Group):
    """
    'child_object_type' of register_based.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity', 'monitor']

    name: name_cls = name_cls
    """
    name child of register_based_child.
    """
    register: register_cls = register_cls
    """
    register child of register_based_child.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of register_based_child.
    """
    active: active_cls = active_cls
    """
    active child of register_based_child.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of register_based_child.
    """
    monitor: monitor_cls = monitor_cls
    """
    monitor child of register_based_child.
    """
