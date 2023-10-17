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
class ribbon_settings(Group):
    """
    'ribbon_settings' child.
    """

    fluent_name = "ribbon-settings"

    child_names = \
        ['field', 'scalefactor']

    field: field_cls = field_cls
    """
    field child of ribbon_settings.
    """
    scalefactor: scalefactor_cls = scalefactor_cls
    """
    scalefactor child of ribbon_settings.
    """
