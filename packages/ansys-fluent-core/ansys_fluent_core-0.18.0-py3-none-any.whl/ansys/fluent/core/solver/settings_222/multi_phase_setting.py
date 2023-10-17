#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_2 import enable as enable_cls
from .options_3 import options as options_cls
class multi_phase_setting(Group):
    """
    'multi_phase_setting' child.
    """

    fluent_name = "multi-phase-setting"

    child_names = \
        ['enable', 'options']

    enable: enable_cls = enable_cls
    """
    enable child of multi_phase_setting.
    """
    options: options_cls = options_cls
    """
    options child of multi_phase_setting.
    """
