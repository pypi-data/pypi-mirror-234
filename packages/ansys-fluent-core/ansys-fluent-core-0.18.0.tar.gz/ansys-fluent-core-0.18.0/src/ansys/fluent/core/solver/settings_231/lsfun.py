#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .value import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class lsfun(Group):
    """
    'lsfun' child.
    """

    fluent_name = "lsfun"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of lsfun.
    """
    value: value_cls = value_cls
    """
    value child of lsfun.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of lsfun.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of lsfun.
    """
    udf: udf_cls = udf_cls
    """
    udf child of lsfun.
    """
