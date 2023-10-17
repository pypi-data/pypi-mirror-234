#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .ddpm_phase import ddpm_phase as ddpm_phase_cls
class volume_displacement(Group):
    """
    'volume_displacement' child.
    """

    fluent_name = "volume-displacement"

    child_names = \
        ['option', 'ddpm_phase']

    option: option_cls = option_cls
    """
    option child of volume_displacement.
    """
    ddpm_phase: ddpm_phase_cls = ddpm_phase_cls
    """
    ddpm_phase child of volume_displacement.
    """
