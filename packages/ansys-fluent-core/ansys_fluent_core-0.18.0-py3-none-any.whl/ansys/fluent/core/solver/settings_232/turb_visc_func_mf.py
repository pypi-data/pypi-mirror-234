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
from .turb_visc_func_mf_child import turb_visc_func_mf_child

class turb_visc_func_mf(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'turb_visc_func_mf' child.
    """

    fluent_name = "turb-visc-func-mf"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of turb_visc_func_mf.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of turb_visc_func_mf.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of turb_visc_func_mf.
    """
    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of turb_visc_func_mf.
    """
