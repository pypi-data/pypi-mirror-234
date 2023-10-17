#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .forward_scattering_factor import forward_scattering_factor as forward_scattering_factor_cls
from .asymmetry_factor import asymmetry_factor as asymmetry_factor_cls
class delta_eddington(Group):
    """
    'delta_eddington' child.
    """

    fluent_name = "delta-eddington"

    child_names = \
        ['forward_scattering_factor', 'asymmetry_factor']

    forward_scattering_factor: forward_scattering_factor_cls = forward_scattering_factor_cls
    """
    forward_scattering_factor child of delta_eddington.
    """
    asymmetry_factor: asymmetry_factor_cls = asymmetry_factor_cls
    """
    asymmetry_factor child of delta_eddington.
    """
