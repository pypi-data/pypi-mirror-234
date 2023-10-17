#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_11 import option as option_cls
from .change_all_o2o_si_names import change_all_o2o_si_names as change_all_o2o_si_names_cls
class naming_option(Command):
    """
    Specify whether or not to include an informative suffix to the mesh interface name.
    
    Parameters
    ----------
        option : int
            'option' child.
        change_all_o2o_si_names : bool
            'change_all_o2o_si_names' child.
    
    """

    fluent_name = "naming-option"

    argument_names = \
        ['option', 'change_all_o2o_si_names']

    option: option_cls = option_cls
    """
    option argument of naming_option.
    """
    change_all_o2o_si_names: change_all_o2o_si_names_cls = change_all_o2o_si_names_cls
    """
    change_all_o2o_si_names argument of naming_option.
    """
