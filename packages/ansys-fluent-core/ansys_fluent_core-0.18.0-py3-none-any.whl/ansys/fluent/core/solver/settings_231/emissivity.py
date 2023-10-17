#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .value import value as value_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class emissivity(Group):
    """
    'emissivity' child.
    """

    fluent_name = "emissivity"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of emissivity.
    """
    value: value_cls = value_cls
    """
    value child of emissivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of emissivity.
    """
