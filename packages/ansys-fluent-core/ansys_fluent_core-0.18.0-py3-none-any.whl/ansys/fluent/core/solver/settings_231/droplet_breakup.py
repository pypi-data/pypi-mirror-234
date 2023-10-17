#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .constant_y0 import constant_y0 as constant_y0_cls
from .number_of_child_droplets import number_of_child_droplets as number_of_child_droplets_cls
from .constant_b1 import constant_b1 as constant_b1_cls
from .constant_b0 import constant_b0 as constant_b0_cls
from .constant_cl import constant_cl as constant_cl_cls
from .constant_ctau import constant_ctau as constant_ctau_cls
from .constant_crt import constant_crt as constant_crt_cls
from .critical_weber_number import critical_weber_number as critical_weber_number_cls
from .core_b1 import core_b1 as core_b1_cls
from .constant_xi import constant_xi as constant_xi_cls
from .target_number_in_parcel import target_number_in_parcel as target_number_in_parcel_cls
from .constant_c0 import constant_c0 as constant_c0_cls
from .column_drag_coeff import column_drag_coeff as column_drag_coeff_cls
from .ligament_factor import ligament_factor as ligament_factor_cls
from .jet_diameter import jet_diameter as jet_diameter_cls
from .constant_k1 import constant_k1 as constant_k1_cls
from .constant_k2 import constant_k2 as constant_k2_cls
from .constant_tb import constant_tb as constant_tb_cls
class droplet_breakup(Group):
    """
    'droplet_breakup' child.
    """

    fluent_name = "droplet-breakup"

    child_names = \
        ['option', 'constant_y0', 'number_of_child_droplets', 'constant_b1',
         'constant_b0', 'constant_cl', 'constant_ctau', 'constant_crt',
         'critical_weber_number', 'core_b1', 'constant_xi',
         'target_number_in_parcel', 'constant_c0', 'column_drag_coeff',
         'ligament_factor', 'jet_diameter', 'constant_k1', 'constant_k2',
         'constant_tb']

    option: option_cls = option_cls
    """
    option child of droplet_breakup.
    """
    constant_y0: constant_y0_cls = constant_y0_cls
    """
    constant_y0 child of droplet_breakup.
    """
    number_of_child_droplets: number_of_child_droplets_cls = number_of_child_droplets_cls
    """
    number_of_child_droplets child of droplet_breakup.
    """
    constant_b1: constant_b1_cls = constant_b1_cls
    """
    constant_b1 child of droplet_breakup.
    """
    constant_b0: constant_b0_cls = constant_b0_cls
    """
    constant_b0 child of droplet_breakup.
    """
    constant_cl: constant_cl_cls = constant_cl_cls
    """
    constant_cl child of droplet_breakup.
    """
    constant_ctau: constant_ctau_cls = constant_ctau_cls
    """
    constant_ctau child of droplet_breakup.
    """
    constant_crt: constant_crt_cls = constant_crt_cls
    """
    constant_crt child of droplet_breakup.
    """
    critical_weber_number: critical_weber_number_cls = critical_weber_number_cls
    """
    critical_weber_number child of droplet_breakup.
    """
    core_b1: core_b1_cls = core_b1_cls
    """
    core_b1 child of droplet_breakup.
    """
    constant_xi: constant_xi_cls = constant_xi_cls
    """
    constant_xi child of droplet_breakup.
    """
    target_number_in_parcel: target_number_in_parcel_cls = target_number_in_parcel_cls
    """
    target_number_in_parcel child of droplet_breakup.
    """
    constant_c0: constant_c0_cls = constant_c0_cls
    """
    constant_c0 child of droplet_breakup.
    """
    column_drag_coeff: column_drag_coeff_cls = column_drag_coeff_cls
    """
    column_drag_coeff child of droplet_breakup.
    """
    ligament_factor: ligament_factor_cls = ligament_factor_cls
    """
    ligament_factor child of droplet_breakup.
    """
    jet_diameter: jet_diameter_cls = jet_diameter_cls
    """
    jet_diameter child of droplet_breakup.
    """
    constant_k1: constant_k1_cls = constant_k1_cls
    """
    constant_k1 child of droplet_breakup.
    """
    constant_k2: constant_k2_cls = constant_k2_cls
    """
    constant_k2 child of droplet_breakup.
    """
    constant_tb: constant_tb_cls = constant_tb_cls
    """
    constant_tb child of droplet_breakup.
    """
