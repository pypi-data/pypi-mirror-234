#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .setting_type import setting_type as setting_type_cls
class modified_setting(Command):
    """
    Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.
    
    Parameters
    ----------
        setting_type : typing.List[str]
            'setting_type' child.
    
    """

    fluent_name = "modified-setting"

    argument_names = \
        ['setting_type']

    setting_type: setting_type_cls = setting_type_cls
    """
    setting_type argument of modified_setting.
    """
