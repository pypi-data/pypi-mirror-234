#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .smooth import smooth as smooth_cls
from .banded import banded as banded_cls
class coloring(Group):
    """
    'coloring' child.
    """

    fluent_name = "coloring"

    child_names = \
        ['option', 'smooth', 'banded']

    option: option_cls = option_cls
    """
    option child of coloring.
    """
    smooth: smooth_cls = smooth_cls
    """
    smooth child of coloring.
    """
    banded: banded_cls = banded_cls
    """
    banded child of coloring.
    """
