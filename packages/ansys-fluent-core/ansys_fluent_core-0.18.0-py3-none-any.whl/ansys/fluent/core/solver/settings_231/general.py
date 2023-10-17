#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solver import solver as solver_cls
from .adjust_solver_defaults_based_on_setup import adjust_solver_defaults_based_on_setup as adjust_solver_defaults_based_on_setup_cls
from .gravity import gravity as gravity_cls
class general(Group):
    """
    'general' child.
    """

    fluent_name = "general"

    child_names = \
        ['solver', 'adjust_solver_defaults_based_on_setup', 'gravity']

    solver: solver_cls = solver_cls
    """
    solver child of general.
    """
    adjust_solver_defaults_based_on_setup: adjust_solver_defaults_based_on_setup_cls = adjust_solver_defaults_based_on_setup_cls
    """
    adjust_solver_defaults_based_on_setup child of general.
    """
    gravity: gravity_cls = gravity_cls
    """
    gravity child of general.
    """
