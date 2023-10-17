#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .histogram_options import histogram_options as histogram_options_cls
from .histogram_parameters import histogram_parameters as histogram_parameters_cls
from .plot_write_sample import plot_write_sample as plot_write_sample_cls
from .reduction import reduction as reduction_cls
from .compute_sample import compute_sample as compute_sample_cls
from .delete_sample import delete_sample as delete_sample_cls
from .list_samples import list_samples as list_samples_cls
from .read_sample_file import read_sample_file as read_sample_file_cls
from .dpm_sample_contour_plots import dpm_sample_contour_plots as dpm_sample_contour_plots_cls
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    child_names = \
        ['histogram_options', 'histogram_parameters', 'plot_write_sample',
         'reduction']

    histogram_options: histogram_options_cls = histogram_options_cls
    """
    histogram_options child of histogram.
    """
    histogram_parameters: histogram_parameters_cls = histogram_parameters_cls
    """
    histogram_parameters child of histogram.
    """
    plot_write_sample: plot_write_sample_cls = plot_write_sample_cls
    """
    plot_write_sample child of histogram.
    """
    reduction: reduction_cls = reduction_cls
    """
    reduction child of histogram.
    """
    command_names = \
        ['compute_sample', 'delete_sample', 'list_samples',
         'read_sample_file', 'dpm_sample_contour_plots']

    compute_sample: compute_sample_cls = compute_sample_cls
    """
    compute_sample command of histogram.
    """
    delete_sample: delete_sample_cls = delete_sample_cls
    """
    delete_sample command of histogram.
    """
    list_samples: list_samples_cls = list_samples_cls
    """
    list_samples command of histogram.
    """
    read_sample_file: read_sample_file_cls = read_sample_file_cls
    """
    read_sample_file command of histogram.
    """
    dpm_sample_contour_plots: dpm_sample_contour_plots_cls = dpm_sample_contour_plots_cls
    """
    dpm_sample_contour_plots command of histogram.
    """
