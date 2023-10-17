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
class film_vapo_rate(Group):
    """
    'film_vapo_rate' child.
    """

    fluent_name = "film-vapo-rate"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of film_vapo_rate.
    """
    constant: constant_cls = constant_cls
    """
    constant child of film_vapo_rate.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of film_vapo_rate.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of film_vapo_rate.
    """
    udf: udf_cls = udf_cls
    """
    udf child of film_vapo_rate.
    """
