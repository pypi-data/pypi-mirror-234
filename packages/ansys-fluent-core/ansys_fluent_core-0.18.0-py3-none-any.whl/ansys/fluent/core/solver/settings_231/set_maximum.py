#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sample_var import sample_var as sample_var_cls
from .max_val import max_val as max_val_cls
class set_maximum(Command):
    """
    'set_maximum' command.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        max_val : real
            'max_val' child.
    
    """

    fluent_name = "set-maximum"

    argument_names = \
        ['sample_var', 'max_val']

    sample_var: sample_var_cls = sample_var_cls
    """
    sample_var argument of set_maximum.
    """
    max_val: max_val_cls = max_val_cls
    """
    max_val argument of set_maximum.
    """
