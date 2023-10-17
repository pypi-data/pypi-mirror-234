#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .default import default as default_cls
from .reverse import reverse as reverse_cls
class curve_length(Group):
    """
    'curve_length' child.
    """

    fluent_name = "curve-length"

    child_names = \
        ['option', 'default', 'reverse']

    option: option_cls = option_cls
    """
    option child of curve_length.
    """
    default: default_cls = default_cls
    """
    default child of curve_length.
    """
    reverse: reverse_cls = reverse_cls
    """
    reverse child of curve_length.
    """
