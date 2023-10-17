#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .loaded_samples import loaded_samples as loaded_samples_cls
from .variable_to_sampled import variable_to_sampled as variable_to_sampled_cls
from .weighting_var import weighting_var as weighting_var_cls
from .correlation_var import correlation_var as correlation_var_cls
from .read_fn import read_fn as read_fn_cls
from .overwrite import overwrite as overwrite_cls
class write_sample(Command):
    """
    'write_sample' command.
    
    Parameters
    ----------
        loaded_samples : str
            'loaded_samples' child.
        variable_to_sampled : str
            'variable_to_sampled' child.
        weighting_var : str
            'weighting_var' child.
        correlation_var : str
            'correlation_var' child.
        read_fn : str
            'read_fn' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "write-sample"

    argument_names = \
        ['loaded_samples', 'variable_to_sampled', 'weighting_var',
         'correlation_var', 'read_fn', 'overwrite']

    loaded_samples: loaded_samples_cls = loaded_samples_cls
    """
    loaded_samples argument of write_sample.
    """
    variable_to_sampled: variable_to_sampled_cls = variable_to_sampled_cls
    """
    variable_to_sampled argument of write_sample.
    """
    weighting_var: weighting_var_cls = weighting_var_cls
    """
    weighting_var argument of write_sample.
    """
    correlation_var: correlation_var_cls = correlation_var_cls
    """
    correlation_var argument of write_sample.
    """
    read_fn: read_fn_cls = read_fn_cls
    """
    read_fn argument of write_sample.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of write_sample.
    """
