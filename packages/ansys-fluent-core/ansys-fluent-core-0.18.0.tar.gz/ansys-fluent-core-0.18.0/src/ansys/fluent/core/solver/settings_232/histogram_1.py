#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .print_3 import print as print_cls
from .write_2 import write as write_cls
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    command_names = \
        ['print', 'write']

    print: print_cls = print_cls
    """
    print command of histogram.
    """
    write: write_cls = write_cls
    """
    write command of histogram.
    """
