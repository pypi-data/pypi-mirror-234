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
from .orthotropic_structure_ym import orthotropic_structure_ym as orthotropic_structure_ym_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class struct_youngs_modulus(Group):
    """
    'struct_youngs_modulus' child.
    """

    fluent_name = "struct-youngs-modulus"

    child_names = \
        ['option', 'value', 'orthotropic_structure_ym',
         'user_defined_function']

    option: option_cls = option_cls
    """
    option child of struct_youngs_modulus.
    """
    value: value_cls = value_cls
    """
    value child of struct_youngs_modulus.
    """
    orthotropic_structure_ym: orthotropic_structure_ym_cls = orthotropic_structure_ym_cls
    """
    orthotropic_structure_ym child of struct_youngs_modulus.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of struct_youngs_modulus.
    """
