#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use import use as use_cls
from .threshold import threshold as threshold_cls
class mesh_adaption(Group):
    """
    Use load balancing for mesh adaption?.
    """

    fluent_name = "mesh-adaption"

    child_names = \
        ['use', 'threshold']

    use: use_cls = use_cls
    """
    use child of mesh_adaption.
    """
    threshold: threshold_cls = threshold_cls
    """
    threshold child of mesh_adaption.
    """
