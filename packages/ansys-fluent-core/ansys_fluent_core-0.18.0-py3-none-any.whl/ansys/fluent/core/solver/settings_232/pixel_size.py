#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .width_1 import width as width_cls
from .height_1 import height as height_cls
from .margin_1 import margin as margin_cls
class pixel_size(Group):
    """
    'pixel_size' child.
    """

    fluent_name = "pixel-size"

    child_names = \
        ['width', 'height', 'margin']

    width: width_cls = width_cls
    """
    width child of pixel_size.
    """
    height: height_cls = height_cls
    """
    height child of pixel_size.
    """
    margin: margin_cls = margin_cls
    """
    margin child of pixel_size.
    """
