#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .across_zones import across_zones as across_zones_cls
from .method_2 import method as method_cls
from .load_vector import load_vector as load_vector_cls
from .pre_test import pre_test as pre_test_cls
from .use_case_file_method import use_case_file_method as use_case_file_method_cls
class auto(Group):
    """
    Enter the menu to set auto partition parameters.
    """

    fluent_name = "auto"

    child_names = \
        ['across_zones', 'method', 'load_vector', 'pre_test']

    across_zones: across_zones_cls = across_zones_cls
    """
    across_zones child of auto.
    """
    method: method_cls = method_cls
    """
    method child of auto.
    """
    load_vector: load_vector_cls = load_vector_cls
    """
    load_vector child of auto.
    """
    pre_test: pre_test_cls = pre_test_cls
    """
    pre_test child of auto.
    """
    command_names = \
        ['use_case_file_method']

    use_case_file_method: use_case_file_method_cls = use_case_file_method_cls
    """
    use_case_file_method command of auto.
    """
