#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .embedded_face_zone import embedded_face_zone as embedded_face_zone_cls
from .floating_surface import floating_surface as floating_surface_cls
class disk_id(Group):
    """
    Menu to define the disk face/surface name:
    
     - embedded-face-zone: select embedded-face-zone name, 
     - floating-disk	: select floating-surface name, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-id"

    child_names = \
        ['embedded_face_zone', 'floating_surface']

    embedded_face_zone: embedded_face_zone_cls = embedded_face_zone_cls
    """
    embedded_face_zone child of disk_id.
    """
    floating_surface: floating_surface_cls = floating_surface_cls
    """
    floating_surface child of disk_id.
    """
