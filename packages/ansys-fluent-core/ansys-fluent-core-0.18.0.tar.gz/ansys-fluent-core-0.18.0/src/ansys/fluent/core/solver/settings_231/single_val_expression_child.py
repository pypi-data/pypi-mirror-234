#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .define import define as define_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls
class single_val_expression_child(Group):
    """
    'child_object_type' of single_val_expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'list_valid_report_names', 'define',
         'average_over', 'old_props']

    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of single_val_expression_child.
    """
    list_valid_report_names: list_valid_report_names_cls = list_valid_report_names_cls
    """
    list_valid_report_names child of single_val_expression_child.
    """
    define: define_cls = define_cls
    """
    define child of single_val_expression_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of single_val_expression_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of single_val_expression_child.
    """
