#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .plane_surface import plane_surface as plane_surface_cls
class surfaces(Group):
    """
    'surfaces' child.
    """

    fluent_name = "surfaces"

    child_names = \
        ['plane_surface']

    plane_surface: plane_surface_cls = plane_surface_cls
    """
    plane_surface child of surfaces.
    """
