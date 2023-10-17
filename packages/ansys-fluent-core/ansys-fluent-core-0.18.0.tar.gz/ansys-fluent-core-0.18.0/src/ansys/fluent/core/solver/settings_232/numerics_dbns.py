#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .first_to_second_order_blending_dbns import first_to_second_order_blending_dbns as first_to_second_order_blending_dbns_cls
class numerics_dbns(Group):
    """
    'numerics_dbns' child.
    """

    fluent_name = "numerics-dbns"

    child_names = \
        ['first_to_second_order_blending_dbns']

    first_to_second_order_blending_dbns: first_to_second_order_blending_dbns_cls = first_to_second_order_blending_dbns_cls
    """
    first_to_second_order_blending_dbns child of numerics_dbns.
    """
