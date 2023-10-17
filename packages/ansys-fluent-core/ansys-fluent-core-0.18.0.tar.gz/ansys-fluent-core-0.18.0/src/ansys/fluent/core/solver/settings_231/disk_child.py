#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .general_1 import general as general_cls
from .geometry_1 import geometry as geometry_cls
from .trimming import trimming as trimming_cls
class disk_child(Group):
    """
    'child_object_type' of disk.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['general', 'geometry', 'trimming']

    general: general_cls = general_cls
    """
    general child of disk_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of disk_child.
    """
    trimming: trimming_cls = trimming_cls
    """
    trimming child of disk_child.
    """
