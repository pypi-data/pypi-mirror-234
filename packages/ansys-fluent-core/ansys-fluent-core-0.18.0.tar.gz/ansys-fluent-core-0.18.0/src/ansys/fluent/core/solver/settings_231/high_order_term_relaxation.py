#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_5 import enable as enable_cls
from .options_3 import options as options_cls
class high_order_term_relaxation(Group):
    """
    Enter High Order Relaxation Menu.
    """

    fluent_name = "high-order-term-relaxation"

    child_names = \
        ['enable', 'options']

    enable: enable_cls = enable_cls
    """
    enable child of high_order_term_relaxation.
    """
    options: options_cls = options_cls
    """
    options child of high_order_term_relaxation.
    """
