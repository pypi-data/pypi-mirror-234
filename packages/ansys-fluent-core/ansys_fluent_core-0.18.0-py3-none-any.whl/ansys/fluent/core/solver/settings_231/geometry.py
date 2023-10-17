#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .reconstruct_geometry import reconstruct_geometry as reconstruct_geometry_cls
class geometry(Group):
    """
    Enter the adaption geometry menu.
    """

    fluent_name = "geometry"

    child_names = \
        ['reconstruct_geometry']

    reconstruct_geometry: reconstruct_geometry_cls = reconstruct_geometry_cls
    """
    reconstruct_geometry child of geometry.
    """
