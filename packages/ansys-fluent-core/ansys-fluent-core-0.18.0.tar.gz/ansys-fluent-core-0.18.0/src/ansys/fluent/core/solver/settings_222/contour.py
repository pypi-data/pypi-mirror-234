#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display import display as display_cls
from .contour_child import contour_child

class contour(NamedObject[contour_child], _CreatableNamedObjectMixin[contour_child]):
    """
    'contour' child.
    """

    fluent_name = "contour"

    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of contour.
    """
    child_object_type: contour_child = contour_child
    """
    child_object_type of contour.
    """
