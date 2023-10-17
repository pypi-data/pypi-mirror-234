#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .kernel import kernel as kernel_cls
from .gaussian_factor import gaussian_factor as gaussian_factor_cls
class averaging_kernel(Group):
    """
    'averaging_kernel' child.
    """

    fluent_name = "averaging-kernel"

    child_names = \
        ['kernel', 'gaussian_factor']

    kernel: kernel_cls = kernel_cls
    """
    kernel child of averaging_kernel.
    """
    gaussian_factor: gaussian_factor_cls = gaussian_factor_cls
    """
    gaussian_factor child of averaging_kernel.
    """
