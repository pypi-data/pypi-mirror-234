#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_5 import enable as enable_cls
from .turbulent_approximation import turbulent_approximation as turbulent_approximation_cls
class convective_heat_transfer(Group):
    """
    'convective_heat_transfer' child.
    """

    fluent_name = "convective-heat-transfer"

    child_names = \
        ['enable', 'turbulent_approximation']

    enable: enable_cls = enable_cls
    """
    enable child of convective_heat_transfer.
    """
    turbulent_approximation: turbulent_approximation_cls = turbulent_approximation_cls
    """
    turbulent_approximation child of convective_heat_transfer.
    """
