#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .all import all as all_cls
from .feature import feature as feature_cls
from .outline import outline as outline_cls
class edge_type(Group):
    """
    'edge_type' child.
    """

    fluent_name = "edge-type"

    child_names = \
        ['option', 'all', 'feature', 'outline']

    option: option_cls = option_cls
    """
    option child of edge_type.
    """
    all: all_cls = all_cls
    """
    all child of edge_type.
    """
    feature: feature_cls = feature_cls
    """
    feature child of edge_type.
    """
    outline: outline_cls = outline_cls
    """
    outline child of edge_type.
    """
