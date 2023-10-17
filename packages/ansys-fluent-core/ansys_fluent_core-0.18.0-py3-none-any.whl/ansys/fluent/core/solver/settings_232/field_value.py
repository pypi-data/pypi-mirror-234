#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .field import field as field_cls
from .option_12 import option as option_cls
from .scaling import scaling as scaling_cls
from .derivative import derivative as derivative_cls
from .size_ratio import size_ratio as size_ratio_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class field_value(Group):
    """
    'field_value' child.
    """

    fluent_name = "field-value"

    child_names = \
        ['field', 'option', 'scaling', 'derivative', 'size_ratio',
         'create_volume_surface']

    field: field_cls = field_cls
    """
    field child of field_value.
    """
    option: option_cls = option_cls
    """
    option child of field_value.
    """
    scaling: scaling_cls = scaling_cls
    """
    scaling child of field_value.
    """
    derivative: derivative_cls = derivative_cls
    """
    derivative child of field_value.
    """
    size_ratio: size_ratio_cls = size_ratio_cls
    """
    size_ratio child of field_value.
    """
    create_volume_surface: create_volume_surface_cls = create_volume_surface_cls
    """
    create_volume_surface child of field_value.
    """
