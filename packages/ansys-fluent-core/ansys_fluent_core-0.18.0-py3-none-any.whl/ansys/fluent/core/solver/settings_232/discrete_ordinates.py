#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .n_theta_divisions import n_theta_divisions as n_theta_divisions_cls
from .n_phi_divisions import n_phi_divisions as n_phi_divisions_cls
from .n_theta_pixels import n_theta_pixels as n_theta_pixels_cls
from .n_phi_pixels import n_phi_pixels as n_phi_pixels_cls
from .do_acceleration import do_acceleration as do_acceleration_cls
from .do_energy_coupling import do_energy_coupling as do_energy_coupling_cls
from .method_partially_specular_wall import method_partially_specular_wall as method_partially_specular_wall_cls
from .fast_second_order_discrete_ordinate import fast_second_order_discrete_ordinate as fast_second_order_discrete_ordinate_cls
from .blending_factor import blending_factor as blending_factor_cls
class discrete_ordinates(Group):
    """
    Enable/disable the discrete ordinates radiation model.
    """

    fluent_name = "discrete-ordinates"

    child_names = \
        ['n_theta_divisions', 'n_phi_divisions', 'n_theta_pixels',
         'n_phi_pixels', 'do_acceleration', 'do_energy_coupling',
         'method_partially_specular_wall',
         'fast_second_order_discrete_ordinate', 'blending_factor']

    n_theta_divisions: n_theta_divisions_cls = n_theta_divisions_cls
    """
    n_theta_divisions child of discrete_ordinates.
    """
    n_phi_divisions: n_phi_divisions_cls = n_phi_divisions_cls
    """
    n_phi_divisions child of discrete_ordinates.
    """
    n_theta_pixels: n_theta_pixels_cls = n_theta_pixels_cls
    """
    n_theta_pixels child of discrete_ordinates.
    """
    n_phi_pixels: n_phi_pixels_cls = n_phi_pixels_cls
    """
    n_phi_pixels child of discrete_ordinates.
    """
    do_acceleration: do_acceleration_cls = do_acceleration_cls
    """
    do_acceleration child of discrete_ordinates.
    """
    do_energy_coupling: do_energy_coupling_cls = do_energy_coupling_cls
    """
    do_energy_coupling child of discrete_ordinates.
    """
    method_partially_specular_wall: method_partially_specular_wall_cls = method_partially_specular_wall_cls
    """
    method_partially_specular_wall child of discrete_ordinates.
    """
    fast_second_order_discrete_ordinate: fast_second_order_discrete_ordinate_cls = fast_second_order_discrete_ordinate_cls
    """
    fast_second_order_discrete_ordinate child of discrete_ordinates.
    """
    blending_factor: blending_factor_cls = blending_factor_cls
    """
    blending_factor child of discrete_ordinates.
    """
