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
class struct_start_temperature(Group):
    """
    'struct_start_temperature' child.
    """

    fluent_name = "struct-start-temperature"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of struct_start_temperature.
    """
    value: value_cls = value_cls
    """
    value child of struct_start_temperature.
    """
