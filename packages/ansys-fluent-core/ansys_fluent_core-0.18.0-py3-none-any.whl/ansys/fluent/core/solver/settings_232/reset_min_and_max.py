#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sample_var import sample_var as sample_var_cls
from .reset_range import reset_range as reset_range_cls
class reset_min_and_max(Command):
    """
    Reset the min and max values of the range to be considered for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        reset_range : bool
            'reset_range' child.
    
    """

    fluent_name = "reset-min-and-max"

    argument_names = \
        ['sample_var', 'reset_range']

    sample_var: sample_var_cls = sample_var_cls
    """
    sample_var argument of reset_min_and_max.
    """
    reset_range: reset_range_cls = reset_range_cls
    """
    reset_range argument of reset_min_and_max.
    """
