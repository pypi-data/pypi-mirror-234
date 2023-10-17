#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pv_coupling_controls import pv_coupling_controls as pv_coupling_controls_cls
from .pv_coupling_method import pv_coupling_method as pv_coupling_method_cls
from .gradient_controls import gradient_controls as gradient_controls_cls
from .specify_gradient_method import specify_gradient_method as specify_gradient_method_cls
class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['pv_coupling_controls', 'pv_coupling_method', 'gradient_controls',
         'specify_gradient_method']

    pv_coupling_controls: pv_coupling_controls_cls = pv_coupling_controls_cls
    """
    pv_coupling_controls child of methods.
    """
    pv_coupling_method: pv_coupling_method_cls = pv_coupling_method_cls
    """
    pv_coupling_method child of methods.
    """
    gradient_controls: gradient_controls_cls = gradient_controls_cls
    """
    gradient_controls child of methods.
    """
    specify_gradient_method: specify_gradient_method_cls = specify_gradient_method_cls
    """
    specify_gradient_method child of methods.
    """
