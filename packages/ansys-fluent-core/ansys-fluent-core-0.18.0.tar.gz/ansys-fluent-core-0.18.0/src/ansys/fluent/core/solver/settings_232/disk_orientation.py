#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .terminology import terminology as terminology_cls
from .disk_normal_x import disk_normal_x as disk_normal_x_cls
from .disk_normal_y import disk_normal_y as disk_normal_y_cls
from .disk_normal_z import disk_normal_z as disk_normal_z_cls
from .disk_pitch_angle import disk_pitch_angle as disk_pitch_angle_cls
from .disk_bank_angle import disk_bank_angle as disk_bank_angle_cls
class disk_orientation(Group):
    """
    Menu to define the rotor disk orientation.
    
     - terminology      : the terminology to specify the rotor disk orientation: rotor-disk-angles / rotor-disk-normal, 
     - disk-normal-x/yz : rotor-disk-normal components, 
     - disk-pitch-angle : , 
     - disk-bank-angle : , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-orientation"

    child_names = \
        ['terminology', 'disk_normal_x', 'disk_normal_y', 'disk_normal_z',
         'disk_pitch_angle', 'disk_bank_angle']

    terminology: terminology_cls = terminology_cls
    """
    terminology child of disk_orientation.
    """
    disk_normal_x: disk_normal_x_cls = disk_normal_x_cls
    """
    disk_normal_x child of disk_orientation.
    """
    disk_normal_y: disk_normal_y_cls = disk_normal_y_cls
    """
    disk_normal_y child of disk_orientation.
    """
    disk_normal_z: disk_normal_z_cls = disk_normal_z_cls
    """
    disk_normal_z child of disk_orientation.
    """
    disk_pitch_angle: disk_pitch_angle_cls = disk_pitch_angle_cls
    """
    disk_pitch_angle child of disk_orientation.
    """
    disk_bank_angle: disk_bank_angle_cls = disk_bank_angle_cls
    """
    disk_bank_angle child of disk_orientation.
    """
