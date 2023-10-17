#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_6 import enable as enable_cls
from .mode import mode as mode_cls
from .rotor import rotor as rotor_cls
from .apply import apply as apply_cls
class virtual_blade_model(Group):
    """
    Enter the vbm model menu.
    """

    fluent_name = "virtual-blade-model"

    child_names = \
        ['enable', 'mode', 'rotor']

    enable: enable_cls = enable_cls
    """
    enable child of virtual_blade_model.
    """
    mode: mode_cls = mode_cls
    """
    mode child of virtual_blade_model.
    """
    rotor: rotor_cls = rotor_cls
    """
    rotor child of virtual_blade_model.
    """
    command_names = \
        ['apply']

    apply: apply_cls = apply_cls
    """
    apply command of virtual_blade_model.
    """
