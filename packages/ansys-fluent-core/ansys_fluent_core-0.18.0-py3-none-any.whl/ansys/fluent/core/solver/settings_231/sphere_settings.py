#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .scale_2 import scale as scale_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .options_9 import options as options_cls
class sphere_settings(Group):
    """
    'sphere_settings' child.
    """

    fluent_name = "sphere-settings"

    child_names = \
        ['scale', 'sphere_lod', 'options']

    scale: scale_cls = scale_cls
    """
    scale child of sphere_settings.
    """
    sphere_lod: sphere_lod_cls = sphere_lod_cls
    """
    sphere_lod child of sphere_settings.
    """
    options: options_cls = options_cls
    """
    options child of sphere_settings.
    """
