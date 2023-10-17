#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .relaxation_factor import relaxation_factor as relaxation_factor_cls
from .select_variables import select_variables as select_variables_cls
from .type_6 import type as type_cls
class options(Group):
    """
    High Order Term Relaxation Options.
    """

    fluent_name = "options"

    child_names = \
        ['relaxation_factor', 'select_variables', 'type']

    relaxation_factor: relaxation_factor_cls = relaxation_factor_cls
    """
    relaxation_factor child of options.
    """
    select_variables: select_variables_cls = select_variables_cls
    """
    select_variables child of options.
    """
    type: type_cls = type_cls
    """
    type child of options.
    """
