#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_1 import enable as enable_cls
from .disable import disable as disable_cls
from .print import print as print_cls
from .clear import clear as clear_cls
class profile(Group):
    """
    Enter the adaption profile menu.
    """

    fluent_name = "profile"

    command_names = \
        ['enable', 'disable', 'print', 'clear']

    enable: enable_cls = enable_cls
    """
    enable command of profile.
    """
    disable: disable_cls = disable_cls
    """
    disable command of profile.
    """
    print: print_cls = print_cls
    """
    print command of profile.
    """
    clear: clear_cls = clear_cls
    """
    clear command of profile.
    """
