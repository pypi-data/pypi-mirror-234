#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .plot_sample import plot_sample as plot_sample_cls
from .write_sample import write_sample as write_sample_cls
class plot_write_sample(Group):
    """
    'plot_write_sample' child.
    """

    fluent_name = "plot-write-sample"

    command_names = \
        ['plot_sample', 'write_sample']

    plot_sample: plot_sample_cls = plot_sample_cls
    """
    plot_sample command of plot_write_sample.
    """
    write_sample: write_sample_cls = write_sample_cls
    """
    write_sample command of plot_write_sample.
    """
