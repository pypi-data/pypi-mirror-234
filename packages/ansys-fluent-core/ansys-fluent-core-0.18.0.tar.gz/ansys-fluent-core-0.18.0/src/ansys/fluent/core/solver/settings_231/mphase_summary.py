#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .verbosity_option import verbosity_option as verbosity_option_cls
class mphase_summary(Command):
    """
    Multiphase Summary and Recommendations.
    
    Parameters
    ----------
        verbosity_option : str
            'verbosity_option' child.
    
    """

    fluent_name = "mphase-summary"

    argument_names = \
        ['verbosity_option']

    verbosity_option: verbosity_option_cls = verbosity_option_cls
    """
    verbosity_option argument of mphase_summary.
    """
