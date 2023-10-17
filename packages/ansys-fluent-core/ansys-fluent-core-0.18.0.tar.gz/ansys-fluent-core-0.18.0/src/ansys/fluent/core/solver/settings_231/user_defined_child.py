#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .input_params import input_params as input_params_cls
from .function_name import function_name as function_name_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls
class user_defined_child(Group):
    """
    'child_object_type' of user_defined.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'input_params', 'function_name',
         'average_over', 'old_props']

    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of user_defined_child.
    """
    input_params: input_params_cls = input_params_cls
    """
    input_params child of user_defined_child.
    """
    function_name: function_name_cls = function_name_cls
    """
    function_name child of user_defined_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of user_defined_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of user_defined_child.
    """
