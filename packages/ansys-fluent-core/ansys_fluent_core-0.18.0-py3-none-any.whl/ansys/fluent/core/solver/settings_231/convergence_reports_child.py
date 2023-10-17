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
from .previous_values_to_consider import previous_values_to_consider as previous_values_to_consider_cls
from .initial_values_to_ignore import initial_values_to_ignore as initial_values_to_ignore_cls
from .iteration_at_creation_or_edit import iteration_at_creation_or_edit as iteration_at_creation_or_edit_cls
from .stop_criterion import stop_criterion as stop_criterion_cls
from .report_defs_1 import report_defs as report_defs_cls
from .print_1 import print as print_cls
from .plot import plot as plot_cls
from .cov import cov as cov_cls
from .active import active as active_cls
from .x_label import x_label as x_label_cls
from .previous_values import previous_values as previous_values_cls
class convergence_reports_child(Group):
    """
    'child_object_type' of convergence_reports.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'old_props', 'previous_values_to_consider',
         'initial_values_to_ignore', 'iteration_at_creation_or_edit',
         'stop_criterion', 'report_defs', 'print', 'plot', 'cov', 'active',
         'x_label', 'previous_values']

    name: name_cls = name_cls
    """
    name child of convergence_reports_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of convergence_reports_child.
    """
    previous_values_to_consider: previous_values_to_consider_cls = previous_values_to_consider_cls
    """
    previous_values_to_consider child of convergence_reports_child.
    """
    initial_values_to_ignore: initial_values_to_ignore_cls = initial_values_to_ignore_cls
    """
    initial_values_to_ignore child of convergence_reports_child.
    """
    iteration_at_creation_or_edit: iteration_at_creation_or_edit_cls = iteration_at_creation_or_edit_cls
    """
    iteration_at_creation_or_edit child of convergence_reports_child.
    """
    stop_criterion: stop_criterion_cls = stop_criterion_cls
    """
    stop_criterion child of convergence_reports_child.
    """
    report_defs: report_defs_cls = report_defs_cls
    """
    report_defs child of convergence_reports_child.
    """
    print: print_cls = print_cls
    """
    print child of convergence_reports_child.
    """
    plot: plot_cls = plot_cls
    """
    plot child of convergence_reports_child.
    """
    cov: cov_cls = cov_cls
    """
    cov child of convergence_reports_child.
    """
    active: active_cls = active_cls
    """
    active child of convergence_reports_child.
    """
    x_label: x_label_cls = x_label_cls
    """
    x_label child of convergence_reports_child.
    """
    previous_values: previous_values_cls = previous_values_cls
    """
    previous_values child of convergence_reports_child.
    """
