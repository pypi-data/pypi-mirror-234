#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_numerics import change_numerics as change_numerics_cls
class non_conformal_interface_numerics(Group):
    """
    Setting non-conformal numerics options.
    """

    fluent_name = "non-conformal-interface-numerics"

    command_names = \
        ['change_numerics']

    change_numerics: change_numerics_cls = change_numerics_cls
    """
    change_numerics command of non_conformal_interface_numerics.
    """
