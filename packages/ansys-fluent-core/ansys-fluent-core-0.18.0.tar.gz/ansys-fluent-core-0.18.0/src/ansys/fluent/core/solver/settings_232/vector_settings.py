#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .style import style as style_cls
from .vector_length import vector_length as vector_length_cls
from .constant_color import constant_color as constant_color_cls
from .vector_of import vector_of as vector_of_cls
from .scale_2 import scale as scale_cls
from .length_to_head_ratio import length_to_head_ratio as length_to_head_ratio_cls
class vector_settings(Group):
    """
    'vector_settings' child.
    """

    fluent_name = "vector-settings"

    child_names = \
        ['style', 'vector_length', 'constant_color', 'vector_of', 'scale',
         'length_to_head_ratio']

    style: style_cls = style_cls
    """
    style child of vector_settings.
    """
    vector_length: vector_length_cls = vector_length_cls
    """
    vector_length child of vector_settings.
    """
    constant_color: constant_color_cls = constant_color_cls
    """
    constant_color child of vector_settings.
    """
    vector_of: vector_of_cls = vector_of_cls
    """
    vector_of child of vector_settings.
    """
    scale: scale_cls = scale_cls
    """
    scale child of vector_settings.
    """
    length_to_head_ratio: length_to_head_ratio_cls = length_to_head_ratio_cls
    """
    length_to_head_ratio child of vector_settings.
    """
