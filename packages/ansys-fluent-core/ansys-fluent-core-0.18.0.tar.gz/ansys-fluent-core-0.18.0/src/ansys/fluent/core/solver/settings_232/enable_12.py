#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable import enable as enable_cls
from .gradient_correction_mode import gradient_correction_mode as gradient_correction_mode_cls
class enable(Command):
    """
    Enable Warped-Face Gradient Correction.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
        gradient_correction_mode : str
            'gradient_correction_mode' child.
    
    """

    fluent_name = "enable?"

    argument_names = \
        ['enable', 'gradient_correction_mode']

    enable: enable_cls = enable_cls
    """
    enable argument of enable.
    """
    gradient_correction_mode: gradient_correction_mode_cls = gradient_correction_mode_cls
    """
    gradient_correction_mode argument of enable.
    """
