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
from .orthotropic_structure_ym import orthotropic_structure_ym as orthotropic_structure_ym_cls
class struct_youngs_modulus(Group):
    """
    'struct_youngs_modulus' child.
    """

    fluent_name = "struct-youngs-modulus"

    child_names = \
        ['option', 'value', 'orthotropic_structure_ym']

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
