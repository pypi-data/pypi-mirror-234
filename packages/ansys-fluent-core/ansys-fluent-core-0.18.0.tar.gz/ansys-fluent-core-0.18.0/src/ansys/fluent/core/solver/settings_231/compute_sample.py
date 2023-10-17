#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sample import sample as sample_cls
from .variable import variable as variable_cls
class compute_sample(Command):
    """
    Compute minimum/maximum of a sample variable.
    
    Parameters
    ----------
        sample : str
            'sample' child.
        variable : str
            'variable' child.
    
    """

    fluent_name = "compute-sample"

    argument_names = \
        ['sample', 'variable']

    sample: sample_cls = sample_cls
    """
    sample argument of compute_sample.
    """
    variable: variable_cls = variable_cls
    """
    variable argument of compute_sample.
    """
