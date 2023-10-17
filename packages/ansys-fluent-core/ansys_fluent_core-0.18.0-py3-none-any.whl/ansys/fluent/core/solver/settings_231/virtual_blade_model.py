#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_4 import enable as enable_cls
from .mode import mode as mode_cls
from .disk import disk as disk_cls
class virtual_blade_model(Group):
    """
    Enter the vbm model menu.
    """

    fluent_name = "virtual-blade-model"

    child_names = \
        ['enable', 'mode', 'disk']

    enable: enable_cls = enable_cls
    """
    enable child of virtual_blade_model.
    """
    mode: mode_cls = mode_cls
    """
    mode child of virtual_blade_model.
    """
    disk: disk_cls = disk_cls
    """
    disk child of virtual_blade_model.
    """
