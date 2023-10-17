#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .modified_setting import modified_setting as modified_setting_cls
from .write_user_setting import write_user_setting as write_user_setting_cls
class modified_setting_options(Group):
    """
    'modified_setting_options' child.
    """

    fluent_name = "modified-setting-options"

    command_names = \
        ['modified_setting', 'write_user_setting']

    modified_setting: modified_setting_cls = modified_setting_cls
    """
    modified_setting command of modified_setting_options.
    """
    write_user_setting: write_user_setting_cls = write_user_setting_cls
    """
    write_user_setting command of modified_setting_options.
    """
