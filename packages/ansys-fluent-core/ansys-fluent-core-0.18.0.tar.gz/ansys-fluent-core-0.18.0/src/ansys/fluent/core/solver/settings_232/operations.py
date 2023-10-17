#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .coarsen import coarsen as coarsen_cls
from .refine import refine as refine_cls
from .swap import swap as swap_cls
from .move import move as move_cls
class operations(Group):
    """
    Enter the anisotropic adaption operations menu.
    """

    fluent_name = "operations"

    child_names = \
        ['coarsen', 'refine', 'swap', 'move']

    coarsen: coarsen_cls = coarsen_cls
    """
    coarsen child of operations.
    """
    refine: refine_cls = refine_cls
    """
    refine child of operations.
    """
    swap: swap_cls = swap_cls
    """
    swap child of operations.
    """
    move: move_cls = move_cls
    """
    move child of operations.
    """
