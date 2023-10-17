#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .old_props import old_props as old_props_cls
from .file_name import file_name as file_name_cls
from .frequency import frequency as frequency_cls
from .flow_frequency import flow_frequency as flow_frequency_cls
from .itr_index import itr_index as itr_index_cls
from .run_index import run_index as run_index_cls
from .frequency_of import frequency_of as frequency_of_cls
from .report_defs import report_defs as report_defs_cls
from .print_1 import print as print_cls
from .active import active as active_cls
from .write_instantaneous_values import write_instantaneous_values as write_instantaneous_values_cls
class report_files_child(Group):
    """
    'child_object_type' of report_files.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'old_props', 'file_name', 'frequency', 'flow_frequency',
         'itr_index', 'run_index', 'frequency_of', 'report_defs', 'print',
         'active', 'write_instantaneous_values']

    name: name_cls = name_cls
    """
    name child of report_files_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of report_files_child.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name child of report_files_child.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of report_files_child.
    """
    flow_frequency: flow_frequency_cls = flow_frequency_cls
    """
    flow_frequency child of report_files_child.
    """
    itr_index: itr_index_cls = itr_index_cls
    """
    itr_index child of report_files_child.
    """
    run_index: run_index_cls = run_index_cls
    """
    run_index child of report_files_child.
    """
    frequency_of: frequency_of_cls = frequency_of_cls
    """
    frequency_of child of report_files_child.
    """
    report_defs: report_defs_cls = report_defs_cls
    """
    report_defs child of report_files_child.
    """
    print: print_cls = print_cls
    """
    print child of report_files_child.
    """
    active: active_cls = active_cls
    """
    active child of report_files_child.
    """
    write_instantaneous_values: write_instantaneous_values_cls = write_instantaneous_values_cls
    """
    write_instantaneous_values child of report_files_child.
    """
