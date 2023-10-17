#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .auto_scale import auto_scale as auto_scale_cls
from .scale_f import scale_f as scale_f_cls
class scale(Group):
    """
    'scale' child.
    """

    fluent_name = "scale"

    child_names = \
        ['auto_scale', 'scale_f']

    auto_scale: auto_scale_cls = auto_scale_cls
    """
    auto_scale child of scale.
    """
    scale_f: scale_f_cls = scale_f_cls
    """
    scale_f child of scale.
    """
