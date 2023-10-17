#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .field import field as field_cls
from .scalefactor import scalefactor as scalefactor_cls
class ribbon(Group):
    """
    'ribbon' child.
    """

    fluent_name = "ribbon"

    child_names = \
        ['field', 'scalefactor']

    field: field_cls = field_cls
    """
    field child of ribbon.
    """
    scalefactor: scalefactor_cls = scalefactor_cls
    """
    scalefactor child of ribbon.
    """
