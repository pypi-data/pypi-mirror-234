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
from .orthotropic_structure_nu import orthotropic_structure_nu as orthotropic_structure_nu_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class struct_poisson_ratio(Group):
    """
    'struct_poisson_ratio' child.
    """

    fluent_name = "struct-poisson-ratio"

    child_names = \
        ['option', 'value', 'orthotropic_structure_nu',
         'user_defined_function']

    option: option_cls = option_cls
    """
    option child of struct_poisson_ratio.
    """
    value: value_cls = value_cls
    """
    value child of struct_poisson_ratio.
    """
    orthotropic_structure_nu: orthotropic_structure_nu_cls = orthotropic_structure_nu_cls
    """
    orthotropic_structure_nu child of struct_poisson_ratio.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of struct_poisson_ratio.
    """
