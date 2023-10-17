#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_of_smoothing import type_of_smoothing as type_of_smoothing_cls
from .number_of_iterations import number_of_iterations as number_of_iterations_cls
from .relaxtion_factor import relaxtion_factor as relaxtion_factor_cls
from .percentage_of_cells import percentage_of_cells as percentage_of_cells_cls
from .skewness_threshold import skewness_threshold as skewness_threshold_cls
class smooth_mesh(Command):
    """
    Smooth the mesh using quality-based, Laplace or skewness methods.
    
    Parameters
    ----------
        type_of_smoothing : str
            'type_of_smoothing' child.
        number_of_iterations : int
            'number_of_iterations' child.
        relaxtion_factor : real
            'relaxtion_factor' child.
        percentage_of_cells : real
            'percentage_of_cells' child.
        skewness_threshold : real
            'skewness_threshold' child.
    
    """

    fluent_name = "smooth-mesh"

    argument_names = \
        ['type_of_smoothing', 'number_of_iterations', 'relaxtion_factor',
         'percentage_of_cells', 'skewness_threshold']

    type_of_smoothing: type_of_smoothing_cls = type_of_smoothing_cls
    """
    type_of_smoothing argument of smooth_mesh.
    """
    number_of_iterations: number_of_iterations_cls = number_of_iterations_cls
    """
    number_of_iterations argument of smooth_mesh.
    """
    relaxtion_factor: relaxtion_factor_cls = relaxtion_factor_cls
    """
    relaxtion_factor argument of smooth_mesh.
    """
    percentage_of_cells: percentage_of_cells_cls = percentage_of_cells_cls
    """
    percentage_of_cells argument of smooth_mesh.
    """
    skewness_threshold: skewness_threshold_cls = skewness_threshold_cls
    """
    skewness_threshold argument of smooth_mesh.
    """
