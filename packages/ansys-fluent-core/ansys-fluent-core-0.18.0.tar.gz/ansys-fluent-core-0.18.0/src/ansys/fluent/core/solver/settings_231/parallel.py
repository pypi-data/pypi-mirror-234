#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_4 import option as option_cls
from .expert_options import expert_options as expert_options_cls
from .hybrid_options import hybrid_options as hybrid_options_cls
class parallel(Group):
    """
    Main menu to allow users to set options controlling the parallel scheme used when tracking particles. 
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "parallel"

    child_names = \
        ['option', 'expert_options', 'hybrid_options']

    option: option_cls = option_cls
    """
    option child of parallel.
    """
    expert_options: expert_options_cls = expert_options_cls
    """
    expert_options child of parallel.
    """
    hybrid_options: hybrid_options_cls = hybrid_options_cls
    """
    hybrid_options child of parallel.
    """
