#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .relaxation_factor_2 import relaxation_factor as relaxation_factor_cls
from .select_variables import select_variables as select_variables_cls
from .relaxation_options import relaxation_options as relaxation_options_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['relaxation_factor', 'select_variables', 'relaxation_options']

    relaxation_factor: relaxation_factor_cls = relaxation_factor_cls
    """
    relaxation_factor child of options.
    """
    select_variables: select_variables_cls = select_variables_cls
    """
    select_variables child of options.
    """
    relaxation_options: relaxation_options_cls = relaxation_options_cls
    """
    relaxation_options child of options.
    """
