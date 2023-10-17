#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .auto_range_1 import auto_range as auto_range_cls
from .correlation import correlation as correlation_cls
from .cumulation_curve import cumulation_curve as cumulation_curve_cls
from .diameter_statistics import diameter_statistics as diameter_statistics_cls
from .histogram_mode import histogram_mode as histogram_mode_cls
from .percentage import percentage as percentage_cls
from .variable_3 import variable_3 as variable_3_cls
from .logarithmic import logarithmic as logarithmic_cls
from .weighting import weighting as weighting_cls
class histogram_options(Group):
    """
    Enter the settings menu for the histogram.
    """

    fluent_name = "histogram-options"

    child_names = \
        ['auto_range', 'correlation', 'cumulation_curve',
         'diameter_statistics', 'histogram_mode', 'percentage', 'variable_3',
         'logarithmic', 'weighting']

    auto_range: auto_range_cls = auto_range_cls
    """
    auto_range child of histogram_options.
    """
    correlation: correlation_cls = correlation_cls
    """
    correlation child of histogram_options.
    """
    cumulation_curve: cumulation_curve_cls = cumulation_curve_cls
    """
    cumulation_curve child of histogram_options.
    """
    diameter_statistics: diameter_statistics_cls = diameter_statistics_cls
    """
    diameter_statistics child of histogram_options.
    """
    histogram_mode: histogram_mode_cls = histogram_mode_cls
    """
    histogram_mode child of histogram_options.
    """
    percentage: percentage_cls = percentage_cls
    """
    percentage child of histogram_options.
    """
    variable_3: variable_3_cls = variable_3_cls
    """
    variable_3 child of histogram_options.
    """
    logarithmic: logarithmic_cls = logarithmic_cls
    """
    logarithmic child of histogram_options.
    """
    weighting: weighting_cls = weighting_cls
    """
    weighting child of histogram_options.
    """
