#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_4 import option as option_cls
from .tolerance import tolerance as tolerance_cls
from .max_number_of_refinements import max_number_of_refinements as max_number_of_refinements_cls
from .number_of_cells_to_cross import number_of_cells_to_cross as number_of_cells_to_cross_cls
class accuracy_control(Group):
    """
    'accuracy_control' child.
    """

    fluent_name = "accuracy-control"

    child_names = \
        ['option', 'tolerance', 'max_number_of_refinements',
         'number_of_cells_to_cross']

    option: option_cls = option_cls
    """
    option child of accuracy_control.
    """
    tolerance: tolerance_cls = tolerance_cls
    """
    tolerance child of accuracy_control.
    """
    max_number_of_refinements: max_number_of_refinements_cls = max_number_of_refinements_cls
    """
    max_number_of_refinements child of accuracy_control.
    """
    number_of_cells_to_cross: number_of_cells_to_cross_cls = number_of_cells_to_cross_cls
    """
    number_of_cells_to_cross child of accuracy_control.
    """
