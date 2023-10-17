#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .tolerance1 import tolerance1 as tolerance1_cls
from .tolerance2 import tolerance2 as tolerance2_cls
from .update import update as update_cls
class tolerance(Command):
    """
    Specification of mapped interface tolerance.
    
    Parameters
    ----------
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        tolerance1 : real
            'tolerance1' child.
        tolerance2 : real
            'tolerance2' child.
        update : bool
            Update mapped interface with new tolerance.
    
    """

    fluent_name = "tolerance"

    argument_names = \
        ['use_local_edge_length_factor', 'tolerance1', 'tolerance2', 'update']

    use_local_edge_length_factor: use_local_edge_length_factor_cls = use_local_edge_length_factor_cls
    """
    use_local_edge_length_factor argument of tolerance.
    """
    tolerance1: tolerance1_cls = tolerance1_cls
    """
    tolerance1 argument of tolerance.
    """
    tolerance2: tolerance2_cls = tolerance2_cls
    """
    tolerance2 argument of tolerance.
    """
    update: update_cls = update_cls
    """
    update argument of tolerance.
    """
