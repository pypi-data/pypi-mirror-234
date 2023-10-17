#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_turb_damping import enable_turb_damping as enable_turb_damping_cls
from .turb_damping_factor import turb_damping_factor as turb_damping_factor_cls
class turbulence_damping(Group):
    """
    'turbulence_damping' child.
    """

    fluent_name = "turbulence-damping"

    child_names = \
        ['enable_turb_damping', 'turb_damping_factor']

    enable_turb_damping: enable_turb_damping_cls = enable_turb_damping_cls
    """
    enable_turb_damping child of turbulence_damping.
    """
    turb_damping_factor: turb_damping_factor_cls = turb_damping_factor_cls
    """
    turb_damping_factor child of turbulence_damping.
    """
