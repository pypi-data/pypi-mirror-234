#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_6 import option as option_cls
class pressure_gradient_force(Group):
    """
    'pressure_gradient_force' child.
    """

    fluent_name = "pressure-gradient-force"

    child_names = \
        ['option']

    option: option_cls = option_cls
    """
    option child of pressure_gradient_force.
    """
