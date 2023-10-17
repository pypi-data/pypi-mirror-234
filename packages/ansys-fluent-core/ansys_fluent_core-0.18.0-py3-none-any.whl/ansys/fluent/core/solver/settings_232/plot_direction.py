#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .curve_length import curve_length as curve_length_cls
class plot_direction(Group):
    """
    'plot_direction' child.
    """

    fluent_name = "plot-direction"

    child_names = \
        ['option', 'direction_vector', 'curve_length']

    option: option_cls = option_cls
    """
    option child of plot_direction.
    """
    direction_vector: direction_vector_cls = direction_vector_cls
    """
    direction_vector child of plot_direction.
    """
    curve_length: curve_length_cls = curve_length_cls
    """
    curve_length child of plot_direction.
    """
