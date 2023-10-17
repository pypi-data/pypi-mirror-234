#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .constant_1 import constant as constant_cls
from .variable_1 import variable as variable_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'constant', 'variable']

    option: option_cls = option_cls
    """
    option child of options.
    """
    constant: constant_cls = constant_cls
    """
    constant child of options.
    """
    variable: variable_cls = variable_cls
    """
    variable child of options.
    """
