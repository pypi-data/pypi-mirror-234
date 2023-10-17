#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_curr_sample import change_curr_sample as change_curr_sample_cls
from .sample import sample as sample_cls
class pick_sample_to_reduce(Command):
    """
    Pick a sample for which to first set-up and then perform the data reduction.
    
    Parameters
    ----------
        change_curr_sample : bool
            'change_curr_sample' child.
        sample : str
            'sample' child.
    
    """

    fluent_name = "pick-sample-to-reduce"

    argument_names = \
        ['change_curr_sample', 'sample']

    change_curr_sample: change_curr_sample_cls = change_curr_sample_cls
    """
    change_curr_sample argument of pick_sample_to_reduce.
    """
    sample: sample_cls = sample_cls
    """
    sample argument of pick_sample_to_reduce.
    """
