#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .yplus_1 import yplus as yplus_cls
from .ystar import ystar as ystar_cls
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'yplus', 'ystar']

    option: option_cls = option_cls
    """
    option child of option.
    """
    yplus: yplus_cls = yplus_cls
    """
    yplus child of option.
    """
    ystar: ystar_cls = ystar_cls
    """
    ystar child of option.
    """
