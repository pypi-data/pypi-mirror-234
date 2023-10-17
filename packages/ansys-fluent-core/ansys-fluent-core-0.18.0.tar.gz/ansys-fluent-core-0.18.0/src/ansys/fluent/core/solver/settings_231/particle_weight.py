#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use import use as use_cls
from .user_defined_2 import user_defined as user_defined_cls
from .value import value as value_cls
from .hybrid_optimization import hybrid_optimization as hybrid_optimization_cls
class particle_weight(Group):
    """
    Set DPM particle weight.
    """

    fluent_name = "particle-weight"

    child_names = \
        ['use', 'user_defined', 'value', 'hybrid_optimization']

    use: use_cls = use_cls
    """
    use child of particle_weight.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of particle_weight.
    """
    value: value_cls = value_cls
    """
    value child of particle_weight.
    """
    hybrid_optimization: hybrid_optimization_cls = hybrid_optimization_cls
    """
    hybrid_optimization child of particle_weight.
    """
