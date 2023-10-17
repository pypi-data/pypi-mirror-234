#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .definition import definition as definition_cls
from .description import description as description_cls
from .parameterid import parameterid as parameterid_cls
from .parametername import parametername as parametername_cls
from .unit import unit as unit_cls
from .input_parameter import input_parameter as input_parameter_cls
from .output_parameter import output_parameter as output_parameter_cls
from .get_value import get_value as get_value_cls
class named_expressions_child(Group):
    """
    'child_object_type' of named_expressions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'definition', 'description', 'parameterid', 'parametername',
         'unit', 'input_parameter', 'output_parameter']

    name: name_cls = name_cls
    """
    name child of named_expressions_child.
    """
    definition: definition_cls = definition_cls
    """
    definition child of named_expressions_child.
    """
    description: description_cls = description_cls
    """
    description child of named_expressions_child.
    """
    parameterid: parameterid_cls = parameterid_cls
    """
    parameterid child of named_expressions_child.
    """
    parametername: parametername_cls = parametername_cls
    """
    parametername child of named_expressions_child.
    """
    unit: unit_cls = unit_cls
    """
    unit child of named_expressions_child.
    """
    input_parameter: input_parameter_cls = input_parameter_cls
    """
    input_parameter child of named_expressions_child.
    """
    output_parameter: output_parameter_cls = output_parameter_cls
    """
    output_parameter child of named_expressions_child.
    """
    query_names = \
        ['get_value']

    get_value: get_value_cls = get_value_cls
    """
    get_value query of named_expressions_child.
    """
