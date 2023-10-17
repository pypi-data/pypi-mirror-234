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
from .duplicate_2 import duplicate as duplicate_cls
from .create_1 import create_1 as create_1_cls
from .load_case_data import load_case_data as load_case_data_cls
from .set_as_current_1 import set_as_current as set_as_current_cls
from .delete_design_points import delete_design_points as delete_design_points_cls
from .save_journals import save_journals as save_journals_cls
from .clear_generated_data import clear_generated_data as clear_generated_data_cls
from .update_current import update_current as update_current_cls
from .update_all import update_all as update_all_cls
from .update_selected import update_selected as update_selected_cls
from .design_points_child import design_points_child

class design_points(NamedObject[design_points_child], _CreatableNamedObjectMixin[design_points_child]):
    """
    'design_points' child.
    """

    fluent_name = "design-points"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'create_1', 'load_case_data',
         'set_as_current', 'delete_design_points', 'save_journals',
         'clear_generated_data', 'update_current', 'update_all',
         'update_selected']

    list: list_cls = list_cls
    """
    list command of design_points.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of design_points.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of design_points.
    """
    create_1: create_1_cls = create_1_cls
    """
    create_1 command of design_points.
    """
    load_case_data: load_case_data_cls = load_case_data_cls
    """
    load_case_data command of design_points.
    """
    set_as_current: set_as_current_cls = set_as_current_cls
    """
    set_as_current command of design_points.
    """
    delete_design_points: delete_design_points_cls = delete_design_points_cls
    """
    delete_design_points command of design_points.
    """
    save_journals: save_journals_cls = save_journals_cls
    """
    save_journals command of design_points.
    """
    clear_generated_data: clear_generated_data_cls = clear_generated_data_cls
    """
    clear_generated_data command of design_points.
    """
    update_current: update_current_cls = update_current_cls
    """
    update_current command of design_points.
    """
    update_all: update_all_cls = update_all_cls
    """
    update_all command of design_points.
    """
    update_selected: update_selected_cls = update_selected_cls
    """
    update_selected command of design_points.
    """
    child_object_type: design_points_child = design_points_child
    """
    child_object_type of design_points.
    """
