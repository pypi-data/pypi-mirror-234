#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .select_sample import select_sample as select_sample_cls
from .plotting_grid_interval_size import plotting_grid_interval_size as plotting_grid_interval_size_cls
from .prepare_expressions import prepare_expressions as prepare_expressions_cls
class dpm_sample_contour_plots(Group):
    """
    'dpm_sample_contour_plots' child.
    """

    fluent_name = "dpm-sample-contour-plots"

    child_names = \
        ['select_sample', 'plotting_grid_interval_size']

    select_sample: select_sample_cls = select_sample_cls
    """
    select_sample child of dpm_sample_contour_plots.
    """
    plotting_grid_interval_size: plotting_grid_interval_size_cls = plotting_grid_interval_size_cls
    """
    plotting_grid_interval_size child of dpm_sample_contour_plots.
    """
    command_names = \
        ['prepare_expressions']

    prepare_expressions: prepare_expressions_cls = prepare_expressions_cls
    """
    prepare_expressions command of dpm_sample_contour_plots.
    """
