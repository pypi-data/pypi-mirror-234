#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .number_of_iterations import number_of_iterations as number_of_iterations_cls
from .explicit_urf import explicit_urf as explicit_urf_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .initial_pressure import initial_pressure as initial_pressure_cls
from .external_aero import external_aero as external_aero_cls
from .const_velocity import const_velocity as const_velocity_cls
class general_settings(Group):
    """
    Enter the general settings menu.
    """

    fluent_name = "general-settings"

    child_names = \
        ['number_of_iterations', 'explicit_urf', 'reference_frame',
         'initial_pressure', 'external_aero', 'const_velocity']

    number_of_iterations: number_of_iterations_cls = number_of_iterations_cls
    """
    number_of_iterations child of general_settings.
    """
    explicit_urf: explicit_urf_cls = explicit_urf_cls
    """
    explicit_urf child of general_settings.
    """
    reference_frame: reference_frame_cls = reference_frame_cls
    """
    reference_frame child of general_settings.
    """
    initial_pressure: initial_pressure_cls = initial_pressure_cls
    """
    initial_pressure child of general_settings.
    """
    external_aero: external_aero_cls = external_aero_cls
    """
    external_aero child of general_settings.
    """
    const_velocity: const_velocity_cls = const_velocity_cls
    """
    const_velocity child of general_settings.
    """
