#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .repair_1 import repair as repair_cls
from .disable_repair import disable_repair as disable_repair_cls
class repair_face_handedness(Command):
    """
    Correct face handedness at left handed faces if possible.
    
    Parameters
    ----------
        repair : bool
            'repair' child.
        disable_repair : bool
            'disable_repair' child.
    
    """

    fluent_name = "repair-face-handedness"

    argument_names = \
        ['repair', 'disable_repair']

    repair: repair_cls = repair_cls
    """
    repair argument of repair_face_handedness.
    """
    disable_repair: disable_repair_cls = disable_repair_cls
    """
    disable_repair argument of repair_face_handedness.
    """
