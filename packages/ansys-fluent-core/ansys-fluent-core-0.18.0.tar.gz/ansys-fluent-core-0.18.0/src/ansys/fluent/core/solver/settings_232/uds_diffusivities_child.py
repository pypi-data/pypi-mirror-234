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
from .expression import expression as expression_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .anisotropic import anisotropic as anisotropic_cls
from .orthotropic import orthotropic as orthotropic_cls
from .cyl_orthotropic import cyl_orthotropic as cyl_orthotropic_cls
class uds_diffusivities_child(Group):
    """
    'child_object_type' of uds_diffusivities.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'expression', 'polynomial',
         'user_defined_function', 'anisotropic', 'orthotropic',
         'cyl_orthotropic']

    option: option_cls = option_cls
    """
    option child of uds_diffusivities_child.
    """
    value: value_cls = value_cls
    """
    value child of uds_diffusivities_child.
    """
    expression: expression_cls = expression_cls
    """
    expression child of uds_diffusivities_child.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of uds_diffusivities_child.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of uds_diffusivities_child.
    """
    anisotropic: anisotropic_cls = anisotropic_cls
    """
    anisotropic child of uds_diffusivities_child.
    """
    orthotropic: orthotropic_cls = orthotropic_cls
    """
    orthotropic child of uds_diffusivities_child.
    """
    cyl_orthotropic: cyl_orthotropic_cls = cyl_orthotropic_cls
    """
    cyl_orthotropic child of uds_diffusivities_child.
    """
