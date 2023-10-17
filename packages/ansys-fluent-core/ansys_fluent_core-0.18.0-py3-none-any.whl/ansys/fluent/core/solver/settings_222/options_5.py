#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .oil_flow import oil_flow as oil_flow_cls
from .reverse import reverse as reverse_cls
from .node_values_1 import node_values as node_values_cls
from .relative_1 import relative as relative_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['oil_flow', 'reverse', 'node_values', 'relative']

    oil_flow: oil_flow_cls = oil_flow_cls
    """
    oil_flow child of options.
    """
    reverse: reverse_cls = reverse_cls
    """
    reverse child of options.
    """
    node_values: node_values_cls = node_values_cls
    """
    node_values child of options.
    """
    relative: relative_cls = relative_cls
    """
    relative child of options.
    """
