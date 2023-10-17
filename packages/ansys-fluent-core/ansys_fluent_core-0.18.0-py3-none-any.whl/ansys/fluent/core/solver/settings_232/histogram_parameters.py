#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .minimum_val import minimum_val as minimum_val_cls
from .maximum_val import maximum_val as maximum_val_cls
from .division_val import division_val as division_val_cls
class histogram_parameters(Group):
    """
    Enter the parameter menu for the histogram.
    """

    fluent_name = "histogram-parameters"

    child_names = \
        ['minimum_val', 'maximum_val', 'division_val']

    minimum_val: minimum_val_cls = minimum_val_cls
    """
    minimum_val child of histogram_parameters.
    """
    maximum_val: maximum_val_cls = maximum_val_cls
    """
    maximum_val child of histogram_parameters.
    """
    division_val: division_val_cls = division_val_cls
    """
    division_val child of histogram_parameters.
    """
