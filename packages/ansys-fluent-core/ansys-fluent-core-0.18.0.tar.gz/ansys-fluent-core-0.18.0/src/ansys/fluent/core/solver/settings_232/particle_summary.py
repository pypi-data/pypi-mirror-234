#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .injection_names import injection_names as injection_names_cls
class particle_summary(Command):
    """
    Print summary report for all current particles.
    
    Parameters
    ----------
        injection_names : typing.List[str]
            'injection_names' child.
    
    """

    fluent_name = "particle-summary"

    argument_names = \
        ['injection_names']

    injection_names: injection_names_cls = injection_names_cls
    """
    injection_names argument of particle_summary.
    """
