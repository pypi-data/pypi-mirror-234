#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .type_3 import type as type_cls
from .id import id as id_cls
from .normal import normal as normal_cls
from .partition import partition as partition_cls
class automatic(Group):
    """
    'automatic' child.
    """

    fluent_name = "automatic"

    child_names = \
        ['option', 'type', 'id', 'normal', 'partition']

    option: option_cls = option_cls
    """
    option child of automatic.
    """
    type: type_cls = type_cls
    """
    type child of automatic.
    """
    id: id_cls = id_cls
    """
    id child of automatic.
    """
    normal: normal_cls = normal_cls
    """
    normal child of automatic.
    """
    partition: partition_cls = partition_cls
    """
    partition child of automatic.
    """
