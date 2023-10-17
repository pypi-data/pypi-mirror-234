#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .physical_models_2 import physical_models as physical_models_cls
from .dynamic_mesh import dynamic_mesh as dynamic_mesh_cls
from .mesh_adaption import mesh_adaption as mesh_adaption_cls
class load_balance(Group):
    """
    'load_balance' child.
    """

    fluent_name = "load-balance"

    child_names = \
        ['physical_models', 'dynamic_mesh', 'mesh_adaption']

    physical_models: physical_models_cls = physical_models_cls
    """
    physical_models child of load_balance.
    """
    dynamic_mesh: dynamic_mesh_cls = dynamic_mesh_cls
    """
    dynamic_mesh child of load_balance.
    """
    mesh_adaption: mesh_adaption_cls = mesh_adaption_cls
    """
    mesh_adaption child of load_balance.
    """
