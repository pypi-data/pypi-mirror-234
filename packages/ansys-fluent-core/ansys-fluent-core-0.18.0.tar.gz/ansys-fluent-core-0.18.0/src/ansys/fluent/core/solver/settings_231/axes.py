#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .numbers import numbers as numbers_cls
from .rules import rules as rules_cls
from .log_scale_1 import log_scale as log_scale_cls
from .auto_scale_1 import auto_scale as auto_scale_cls
from .labels import labels as labels_cls
class axes(Group):
    """
    'axes' child.
    """

    fluent_name = "axes"

    child_names = \
        ['numbers', 'rules', 'log_scale', 'auto_scale', 'labels']

    numbers: numbers_cls = numbers_cls
    """
    numbers child of axes.
    """
    rules: rules_cls = rules_cls
    """
    rules child of axes.
    """
    log_scale: log_scale_cls = log_scale_cls
    """
    log_scale child of axes.
    """
    auto_scale: auto_scale_cls = auto_scale_cls
    """
    auto_scale child of axes.
    """
    labels: labels_cls = labels_cls
    """
    labels child of axes.
    """
