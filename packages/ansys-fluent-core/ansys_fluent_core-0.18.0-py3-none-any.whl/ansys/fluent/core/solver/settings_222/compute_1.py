#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .compute import compute as compute_cls
class compute(Group):
    """
    'compute' child.
    """

    fluent_name = "compute"

    child_names = \
        ['compute']

    compute: compute_cls = compute_cls
    """
    compute child of compute.
    """
