#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .per_id import per_id as per_id_cls
class make_phaselag_from_periodic(Command):
    """
    Convert periodic interface to phase lagged.
    
    Parameters
    ----------
        per_id : int
            'per_id' child.
    
    """

    fluent_name = "make-phaselag-from-periodic"

    argument_names = \
        ['per_id']

    per_id: per_id_cls = per_id_cls
    """
    per_id argument of make_phaselag_from_periodic.
    """
