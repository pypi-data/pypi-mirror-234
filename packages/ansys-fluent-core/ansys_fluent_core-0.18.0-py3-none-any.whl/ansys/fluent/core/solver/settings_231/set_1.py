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
from .verbosity_6 import verbosity as verbosity_cls
class set(Group):
    """
    Edit a definition for automatic poor mesh numerics.
    """

    fluent_name = "set"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity']

    name: name_cls = name_cls
    """
    name child of set.
    """
    register: register_cls = register_cls
    """
    register child of set.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of set.
    """
    active: active_cls = active_cls
    """
    active child of set.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of set.
    """
