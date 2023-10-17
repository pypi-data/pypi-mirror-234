#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .compressible_liquid import compressible_liquid as compressible_liquid_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .value_1 import value as value_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'compressible_liquid', 'user_defined_function', 'value']

    option: option_cls = option_cls
    """
    option child of density.
    """
    compressible_liquid: compressible_liquid_cls = compressible_liquid_cls
    """
    compressible_liquid child of density.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of density.
    """
    value: value_cls = value_cls
    """
    value child of density.
    """
