#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .constant import constant as constant_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class per_dispz(Group):
    """
    'per_dispz' child.
    """

    fluent_name = "per-dispz"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of per_dispz.
    """
    constant: constant_cls = constant_cls
    """
    constant child of per_dispz.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of per_dispz.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of per_dispz.
    """
    udf: udf_cls = udf_cls
    """
    udf child of per_dispz.
    """
