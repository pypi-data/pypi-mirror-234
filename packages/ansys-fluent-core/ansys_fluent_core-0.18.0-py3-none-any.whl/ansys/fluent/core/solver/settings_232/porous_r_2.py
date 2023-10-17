#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .value_1 import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class porous_r_2(Group):
    """
    'porous_r_2' child.
    """

    fluent_name = "porous-r-2"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of porous_r_2.
    """
    value: value_cls = value_cls
    """
    value child of porous_r_2.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of porous_r_2.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of porous_r_2.
    """
    udf: udf_cls = udf_cls
    """
    udf child of porous_r_2.
    """
