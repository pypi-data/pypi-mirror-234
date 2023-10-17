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
class youngs_modulus_0(Group):
    """
    'youngs_modulus_0' child.
    """

    fluent_name = "youngs-modulus-0"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of youngs_modulus_0.
    """
    value: value_cls = value_cls
    """
    value child of youngs_modulus_0.
    """
