#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .none_1 import none as none_cls
from .gradient_1 import gradient as gradient_cls
from .curvature import curvature as curvature_cls
from .hessian import hessian as hessian_cls
class derivative(Group):
    """
    'derivative' child.
    """

    fluent_name = "derivative"

    child_names = \
        ['option', 'none', 'gradient', 'curvature', 'hessian']

    option: option_cls = option_cls
    """
    option child of derivative.
    """
    none: none_cls = none_cls
    """
    none child of derivative.
    """
    gradient: gradient_cls = gradient_cls
    """
    gradient child of derivative.
    """
    curvature: curvature_cls = curvature_cls
    """
    curvature child of derivative.
    """
    hessian: hessian_cls = hessian_cls
    """
    hessian child of derivative.
    """
