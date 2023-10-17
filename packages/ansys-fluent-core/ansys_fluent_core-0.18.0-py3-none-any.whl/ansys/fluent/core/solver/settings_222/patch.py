#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .vof_smooth_options import vof_smooth_options as vof_smooth_options_cls
class patch(Group):
    """
    'patch' child.
    """

    fluent_name = "patch"

    child_names = \
        ['vof_smooth_options']

    vof_smooth_options: vof_smooth_options_cls = vof_smooth_options_cls
    """
    vof_smooth_options child of patch.
    """
