#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_9 import enable as enable_cls
from .disable_1 import disable as disable_cls
from .copy_2 import copy as copy_cls
from .delete_1 import delete as delete_cls
from .export_1 import export as export_cls
from .import__1 import import_ as import__cls
class execute_commands(Group):
    """
    'execute_commands' child.
    """

    fluent_name = "execute-commands"

    command_names = \
        ['enable', 'disable', 'copy', 'delete', 'export', 'import_']

    enable: enable_cls = enable_cls
    """
    enable command of execute_commands.
    """
    disable: disable_cls = disable_cls
    """
    disable command of execute_commands.
    """
    copy: copy_cls = copy_cls
    """
    copy command of execute_commands.
    """
    delete: delete_cls = delete_cls
    """
    delete command of execute_commands.
    """
    export: export_cls = export_cls
    """
    export command of execute_commands.
    """
    import_: import__cls = import__cls
    """
    import_ command of execute_commands.
    """
