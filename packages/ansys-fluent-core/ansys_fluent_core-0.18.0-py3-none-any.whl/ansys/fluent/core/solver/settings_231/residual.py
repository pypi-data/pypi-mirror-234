#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .equation_for_residual import equation_for_residual as equation_for_residual_cls
from .threshold import threshold as threshold_cls
class residual(Group):
    """
    'residual' child.
    """

    fluent_name = "residual"

    child_names = \
        ['equation_for_residual', 'threshold']

    equation_for_residual: equation_for_residual_cls = equation_for_residual_cls
    """
    equation_for_residual child of residual.
    """
    threshold: threshold_cls = threshold_cls
    """
    threshold child of residual.
    """
