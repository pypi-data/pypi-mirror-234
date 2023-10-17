#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .from_ import from_ as from__cls
from .to import to as to_cls
class duplicate(Command):
    """
    'duplicate' command.
    
    Parameters
    ----------
        from_ : str
            'from' child.
        to : str
            'to' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['from_', 'to']

    from_: from__cls = from__cls
    """
    from_ argument of duplicate.
    """
    to: to_cls = to_cls
    """
    to argument of duplicate.
    """
