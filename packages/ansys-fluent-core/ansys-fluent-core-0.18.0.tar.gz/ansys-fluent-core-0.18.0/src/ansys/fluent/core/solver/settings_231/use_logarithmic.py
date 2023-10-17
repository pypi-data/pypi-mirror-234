#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sample_var import sample_var as sample_var_cls
from .enable_log import enable_log as enable_log_cls
class use_logarithmic(Command):
    """
    Switch on or off logarithmic scaling to be used for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        enable_log : bool
            'enable_log' child.
    
    """

    fluent_name = "use-logarithmic?"

    argument_names = \
        ['sample_var', 'enable_log']

    sample_var: sample_var_cls = sample_var_cls
    """
    sample_var argument of use_logarithmic.
    """
    enable_log: enable_log_cls = enable_log_cls
    """
    enable_log argument of use_logarithmic.
    """
