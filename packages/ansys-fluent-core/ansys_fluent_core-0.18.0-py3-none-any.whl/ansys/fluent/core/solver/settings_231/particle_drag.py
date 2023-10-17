#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .shape_factor import shape_factor as shape_factor_cls
from .cunningham_factor import cunningham_factor as cunningham_factor_cls
class particle_drag(Group):
    """
    'particle_drag' child.
    """

    fluent_name = "particle-drag"

    child_names = \
        ['option', 'shape_factor', 'cunningham_factor']

    option: option_cls = option_cls
    """
    option child of particle_drag.
    """
    shape_factor: shape_factor_cls = shape_factor_cls
    """
    shape_factor child of particle_drag.
    """
    cunningham_factor: cunningham_factor_cls = cunningham_factor_cls
    """
    cunningham_factor child of particle_drag.
    """
