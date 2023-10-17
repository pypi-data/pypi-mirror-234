#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .basic_info import basic_info as basic_info_cls
from .disk_origin import disk_origin as disk_origin_cls
from .disk_orientation import disk_orientation as disk_orientation_cls
from .disk_id import disk_id as disk_id_cls
from .blade_pitch_angles import blade_pitch_angles as blade_pitch_angles_cls
from .blade_flap_angles import blade_flap_angles as blade_flap_angles_cls
from .tip_loss import tip_loss as tip_loss_cls
class general(Group):
    """
    Menu to define the rotor general information.
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "general"

    child_names = \
        ['basic_info', 'disk_origin', 'disk_orientation', 'disk_id',
         'blade_pitch_angles', 'blade_flap_angles', 'tip_loss']

    basic_info: basic_info_cls = basic_info_cls
    """
    basic_info child of general.
    """
    disk_origin: disk_origin_cls = disk_origin_cls
    """
    disk_origin child of general.
    """
    disk_orientation: disk_orientation_cls = disk_orientation_cls
    """
    disk_orientation child of general.
    """
    disk_id: disk_id_cls = disk_id_cls
    """
    disk_id child of general.
    """
    blade_pitch_angles: blade_pitch_angles_cls = blade_pitch_angles_cls
    """
    blade_pitch_angles child of general.
    """
    blade_flap_angles: blade_flap_angles_cls = blade_flap_angles_cls
    """
    blade_flap_angles child of general.
    """
    tip_loss: tip_loss_cls = tip_loss_cls
    """
    tip_loss child of general.
    """
