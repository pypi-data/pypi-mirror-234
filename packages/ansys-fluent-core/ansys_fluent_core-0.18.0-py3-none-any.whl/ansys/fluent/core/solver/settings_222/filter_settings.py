#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .field import field as field_cls
from .options_7 import options as options_cls
from .enabled_2 import enabled as enabled_cls
from .filter_minimum import filter_minimum as filter_minimum_cls
from .filter_maximum import filter_maximum as filter_maximum_cls
class filter_settings(Group):
    """
    'filter_settings' child.
    """

    fluent_name = "filter-settings"

    child_names = \
        ['field', 'options', 'enabled', 'filter_minimum', 'filter_maximum']

    field: field_cls = field_cls
    """
    field child of filter_settings.
    """
    options: options_cls = options_cls
    """
    options child of filter_settings.
    """
    enabled: enabled_cls = enabled_cls
    """
    enabled child of filter_settings.
    """
    filter_minimum: filter_minimum_cls = filter_minimum_cls
    """
    filter_minimum child of filter_settings.
    """
    filter_maximum: filter_maximum_cls = filter_maximum_cls
    """
    filter_maximum child of filter_settings.
    """
