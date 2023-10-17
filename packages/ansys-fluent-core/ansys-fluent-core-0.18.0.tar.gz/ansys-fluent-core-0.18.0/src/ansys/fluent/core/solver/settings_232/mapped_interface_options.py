#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solution_controls import solution_controls as solution_controls_cls
from .tolerance_1 import tolerance as tolerance_cls
from .convert_to_mapped_interface import convert_to_mapped_interface as convert_to_mapped_interface_cls
class mapped_interface_options(Group):
    """
    Enter the mapped-interface-options menu.
    """

    fluent_name = "mapped-interface-options"

    command_names = \
        ['solution_controls', 'tolerance', 'convert_to_mapped_interface']

    solution_controls: solution_controls_cls = solution_controls_cls
    """
    solution_controls command of mapped_interface_options.
    """
    tolerance: tolerance_cls = tolerance_cls
    """
    tolerance command of mapped_interface_options.
    """
    convert_to_mapped_interface: convert_to_mapped_interface_cls = convert_to_mapped_interface_cls
    """
    convert_to_mapped_interface command of mapped_interface_options.
    """
