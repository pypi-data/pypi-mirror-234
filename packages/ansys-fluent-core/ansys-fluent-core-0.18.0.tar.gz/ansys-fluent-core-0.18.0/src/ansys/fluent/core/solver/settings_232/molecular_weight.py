#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
from .rgp_table import rgp_table as rgp_table_cls
class molecular_weight(Group):
    """
    'molecular_weight' child.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['option', 'value', 'rgp_table']

    option: option_cls = option_cls
    """
    option child of molecular_weight.
    """
    value: value_cls = value_cls
    """
    value child of molecular_weight.
    """
    rgp_table: rgp_table_cls = rgp_table_cls
    """
    rgp_table child of molecular_weight.
    """
