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
class diffusivity_reference_pressure(Group):
    """
    'diffusivity_reference_pressure' child.
    """

    fluent_name = "diffusivity-reference-pressure"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of diffusivity_reference_pressure.
    """
    value: value_cls = value_cls
    """
    value child of diffusivity_reference_pressure.
    """
