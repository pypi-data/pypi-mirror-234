#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .automatic import automatic as automatic_cls
from .manual import manual as manual_cls
class coloring(Group):
    """
    'coloring' child.
    """

    fluent_name = "coloring"

    child_names = \
        ['option', 'automatic', 'manual']

    option: option_cls = option_cls
    """
    option child of coloring.
    """
    automatic: automatic_cls = automatic_cls
    """
    automatic child of coloring.
    """
    manual: manual_cls = manual_cls
    """
    manual child of coloring.
    """
