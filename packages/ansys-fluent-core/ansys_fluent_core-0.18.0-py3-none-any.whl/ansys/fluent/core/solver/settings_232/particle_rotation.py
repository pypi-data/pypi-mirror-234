#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable import enable as enable_cls
from .drag_law import drag_law as drag_law_cls
from .lift_law import lift_law as lift_law_cls
class particle_rotation(Group):
    """
    'particle_rotation' child.
    """

    fluent_name = "particle-rotation"

    child_names = \
        ['enable', 'drag_law', 'lift_law']

    enable: enable_cls = enable_cls
    """
    enable child of particle_rotation.
    """
    drag_law: drag_law_cls = drag_law_cls
    """
    drag_law child of particle_rotation.
    """
    lift_law: lift_law_cls = lift_law_cls
    """
    lift_law child of particle_rotation.
    """
