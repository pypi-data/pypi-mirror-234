#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .principal_axes import principal_axes as principal_axes_cls
from .principal_values import principal_values as principal_values_cls
from .conductivity import conductivity as conductivity_cls
class principal_axes_values(Group):
    """
    'principal_axes_values' child.
    """

    fluent_name = "principal-axes-values"

    child_names = \
        ['principal_axes', 'principal_values', 'conductivity']

    principal_axes: principal_axes_cls = principal_axes_cls
    """
    principal_axes child of principal_axes_values.
    """
    principal_values: principal_values_cls = principal_values_cls
    """
    principal_values child of principal_axes_values.
    """
    conductivity: conductivity_cls = conductivity_cls
    """
    conductivity child of principal_axes_values.
    """
