#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_enhancement import use_enhancement as use_enhancement_cls
from .aspect_ratio_1 import aspect_ratio as aspect_ratio_cls
class stretched_mesh_enhancement(Group):
    """
    Enhancement for mesh with stretched cells.
    """

    fluent_name = "stretched-mesh-enhancement"

    child_names = \
        ['use_enhancement', 'aspect_ratio']

    use_enhancement: use_enhancement_cls = use_enhancement_cls
    """
    use_enhancement child of stretched_mesh_enhancement.
    """
    aspect_ratio: aspect_ratio_cls = aspect_ratio_cls
    """
    aspect_ratio child of stretched_mesh_enhancement.
    """
