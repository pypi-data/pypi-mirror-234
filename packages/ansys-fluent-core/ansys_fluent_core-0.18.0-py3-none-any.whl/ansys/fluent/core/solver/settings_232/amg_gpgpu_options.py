#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .amg_gpgpu_options_child import amg_gpgpu_options_child

class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child], _NonCreatableNamedObjectMixin[amg_gpgpu_options_child]):
    """
    'amg_gpgpu_options' child.
    """

    fluent_name = "amg-gpgpu-options"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of amg_gpgpu_options.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of amg_gpgpu_options.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of amg_gpgpu_options.
    """
    child_object_type: amg_gpgpu_options_child = amg_gpgpu_options_child
    """
    child_object_type of amg_gpgpu_options.
    """
