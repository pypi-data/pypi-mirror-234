#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_3 import enable as enable_cls
from .method import method as method_cls
from .value import value as value_cls
from .print_1 import print as print_cls
class operating_density(Group):
    """
    Enable/disable use of a specified operating density.
    """

    fluent_name = "operating-density"

    child_names = \
        ['enable', 'method', 'value']

    enable: enable_cls = enable_cls
    """
    enable child of operating_density.
    """
    method: method_cls = method_cls
    """
    method child of operating_density.
    """
    value: value_cls = value_cls
    """
    value child of operating_density.
    """
    command_names = \
        ['print']

    print: print_cls = print_cls
    """
    print command of operating_density.
    """
