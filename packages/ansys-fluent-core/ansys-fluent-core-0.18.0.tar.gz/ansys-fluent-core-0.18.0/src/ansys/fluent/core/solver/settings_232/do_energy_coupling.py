#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_4 import enable as enable_cls
from .solution_method import solution_method as solution_method_cls
class do_energy_coupling(Group):
    """
    'do_energy_coupling' child.
    """

    fluent_name = "do-energy-coupling"

    child_names = \
        ['enable', 'solution_method']

    enable: enable_cls = enable_cls
    """
    enable child of do_energy_coupling.
    """
    solution_method: solution_method_cls = solution_method_cls
    """
    solution_method child of do_energy_coupling.
    """
