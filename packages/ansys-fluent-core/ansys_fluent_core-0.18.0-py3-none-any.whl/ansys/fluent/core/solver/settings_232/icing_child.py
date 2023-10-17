#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .report_type import report_type as report_type_cls
from .old_props import old_props as old_props_cls
class icing_child(Group):
    """
    'child_object_type' of icing.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'old_props']

    name: name_cls = name_cls
    """
    name child of icing_child.
    """
    report_type: report_type_cls = report_type_cls
    """
    report_type child of icing_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of icing_child.
    """
