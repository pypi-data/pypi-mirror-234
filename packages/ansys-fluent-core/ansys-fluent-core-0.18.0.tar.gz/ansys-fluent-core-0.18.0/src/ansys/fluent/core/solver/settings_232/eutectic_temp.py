#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
class eutectic_temp(Group):
    """
    'eutectic_temp' child.
    """

    fluent_name = "eutectic-temp"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of eutectic_temp.
    """
    value: value_cls = value_cls
    """
    value child of eutectic_temp.
    """
