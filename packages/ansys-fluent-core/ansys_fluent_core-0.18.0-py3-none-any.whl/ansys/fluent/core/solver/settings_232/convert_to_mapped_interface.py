#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .all import all as all_cls
from .auto import auto as auto_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .tolerance1 import tolerance1 as tolerance1_cls
from .tolerance2 import tolerance2 as tolerance2_cls
class convert_to_mapped_interface(Command):
    """
    Convert non-conformal mesh interface to mapped mesh interfaces.
    
    Parameters
    ----------
        all : bool
            Convert all mesh interfaces to mapped mesh interfaces.
        auto : bool
            Convert poorly matching mesh interfaces to mapped mesh interfaces.
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        tolerance1 : real
            'tolerance1' child.
        tolerance2 : real
            'tolerance2' child.
    
    """

    fluent_name = "convert-to-mapped-interface"

    argument_names = \
        ['all', 'auto', 'use_local_edge_length_factor', 'tolerance1',
         'tolerance2']

    all: all_cls = all_cls
    """
    all argument of convert_to_mapped_interface.
    """
    auto: auto_cls = auto_cls
    """
    auto argument of convert_to_mapped_interface.
    """
    use_local_edge_length_factor: use_local_edge_length_factor_cls = use_local_edge_length_factor_cls
    """
    use_local_edge_length_factor argument of convert_to_mapped_interface.
    """
    tolerance1: tolerance1_cls = tolerance1_cls
    """
    tolerance1 argument of convert_to_mapped_interface.
    """
    tolerance2: tolerance2_cls = tolerance2_cls
    """
    tolerance2 argument of convert_to_mapped_interface.
    """
