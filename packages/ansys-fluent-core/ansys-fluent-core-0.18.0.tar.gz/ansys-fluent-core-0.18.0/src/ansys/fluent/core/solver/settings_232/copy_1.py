#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .from_ import from_ as from__cls
from .to_1 import to as to_cls
from .verbosity_3 import verbosity as verbosity_cls
class copy(Command):
    """
    'copy' command.
    
    Parameters
    ----------
        from_ : str
            'from' child.
        to : typing.List[str]
            'to' child.
        verbosity : bool
            'verbosity' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['from_', 'to', 'verbosity']

    from_: from__cls = from__cls
    """
    from_ argument of copy.
    """
    to: to_cls = to_cls
    """
    to argument of copy.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity argument of copy.
    """
