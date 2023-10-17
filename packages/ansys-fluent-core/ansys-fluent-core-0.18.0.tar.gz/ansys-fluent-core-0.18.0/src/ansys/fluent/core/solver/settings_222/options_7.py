#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .inside import inside as inside_cls
from .outside import outside as outside_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'inside', 'outside']

    option: option_cls = option_cls
    """
    option child of options.
    """
    inside: inside_cls = inside_cls
    """
    inside child of options.
    """
    outside: outside_cls = outside_cls
    """
    outside child of options.
    """
