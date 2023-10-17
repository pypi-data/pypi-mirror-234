#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .graphics import graphics as graphics_cls
from .surfaces_1 import surfaces as surfaces_cls
class results(Group):
    """
    'results' child.
    """

    fluent_name = "results"

    child_names = \
        ['graphics', 'surfaces']

    graphics: graphics_cls = graphics_cls
    """
    graphics child of results.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of results.
    """
