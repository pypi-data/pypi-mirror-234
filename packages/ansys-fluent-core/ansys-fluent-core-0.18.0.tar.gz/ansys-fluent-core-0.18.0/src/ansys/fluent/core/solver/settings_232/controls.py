#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .numerical_damping_factor import numerical_damping_factor as numerical_damping_factor_cls
from .enhanced_strain import enhanced_strain as enhanced_strain_cls
from .unsteady_damping_rayleigh import unsteady_damping_rayleigh as unsteady_damping_rayleigh_cls
from .amg_stabilization import amg_stabilization as amg_stabilization_cls
from .max_iter import max_iter as max_iter_cls
class controls(Group):
    """
    Enter the structure controls menu.
    """

    fluent_name = "controls"

    child_names = \
        ['numerical_damping_factor', 'enhanced_strain',
         'unsteady_damping_rayleigh', 'amg_stabilization', 'max_iter']

    numerical_damping_factor: numerical_damping_factor_cls = numerical_damping_factor_cls
    """
    numerical_damping_factor child of controls.
    """
    enhanced_strain: enhanced_strain_cls = enhanced_strain_cls
    """
    enhanced_strain child of controls.
    """
    unsteady_damping_rayleigh: unsteady_damping_rayleigh_cls = unsteady_damping_rayleigh_cls
    """
    unsteady_damping_rayleigh child of controls.
    """
    amg_stabilization: amg_stabilization_cls = amg_stabilization_cls
    """
    amg_stabilization child of controls.
    """
    max_iter: max_iter_cls = max_iter_cls
    """
    max_iter child of controls.
    """
