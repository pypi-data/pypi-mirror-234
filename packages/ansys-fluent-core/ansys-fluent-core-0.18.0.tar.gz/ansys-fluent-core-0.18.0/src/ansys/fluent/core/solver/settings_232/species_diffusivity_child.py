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
from .polynomial import polynomial as polynomial_cls
class species_diffusivity_child(Group):
    """
    'child_object_type' of species_diffusivity.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'polynomial']

    option: option_cls = option_cls
    """
    option child of species_diffusivity_child.
    """
    value: value_cls = value_cls
    """
    value child of species_diffusivity_child.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of species_diffusivity_child.
    """
