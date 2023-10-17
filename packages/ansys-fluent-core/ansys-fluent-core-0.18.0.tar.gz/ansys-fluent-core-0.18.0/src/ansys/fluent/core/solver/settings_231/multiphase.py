#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .models import models as models_cls
from .vaporization_pressure import vaporization_pressure as vaporization_pressure_cls
from .non_condensable_gas import non_condensable_gas as non_condensable_gas_cls
from .liquid_surface_tension import liquid_surface_tension as liquid_surface_tension_cls
from .bubble_number_density import bubble_number_density as bubble_number_density_cls
from .number_of_phases import number_of_phases as number_of_phases_cls
from .number_of_eulerian_discrete_phases import number_of_eulerian_discrete_phases as number_of_eulerian_discrete_phases_cls
class multiphase(Group):
    """
    'multiphase' child.
    """

    fluent_name = "multiphase"

    child_names = \
        ['models', 'vaporization_pressure', 'non_condensable_gas',
         'liquid_surface_tension', 'bubble_number_density',
         'number_of_phases', 'number_of_eulerian_discrete_phases']

    models: models_cls = models_cls
    """
    models child of multiphase.
    """
    vaporization_pressure: vaporization_pressure_cls = vaporization_pressure_cls
    """
    vaporization_pressure child of multiphase.
    """
    non_condensable_gas: non_condensable_gas_cls = non_condensable_gas_cls
    """
    non_condensable_gas child of multiphase.
    """
    liquid_surface_tension: liquid_surface_tension_cls = liquid_surface_tension_cls
    """
    liquid_surface_tension child of multiphase.
    """
    bubble_number_density: bubble_number_density_cls = bubble_number_density_cls
    """
    bubble_number_density child of multiphase.
    """
    number_of_phases: number_of_phases_cls = number_of_phases_cls
    """
    number_of_phases child of multiphase.
    """
    number_of_eulerian_discrete_phases: number_of_eulerian_discrete_phases_cls = number_of_eulerian_discrete_phases_cls
    """
    number_of_eulerian_discrete_phases child of multiphase.
    """
