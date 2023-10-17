#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .print_histogram import print_histogram as print_histogram_cls
from .write_histogram import write_histogram as write_histogram_cls
class print_write_histogram(Group):
    """
    'print_write_histogram' child.
    """

    fluent_name = "print-write-histogram"

    command_names = \
        ['print_histogram', 'write_histogram']

    print_histogram: print_histogram_cls = print_histogram_cls
    """
    print_histogram command of print_write_histogram.
    """
    write_histogram: write_histogram_cls = write_histogram_cls
    """
    write_histogram command of print_write_histogram.
    """
