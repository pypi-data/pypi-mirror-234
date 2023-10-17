#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .from_name import from_name as from_name_cls
from .new_name import new_name as new_name_cls
class copy(Command):
    """
    Copy graphics object.
    
    Parameters
    ----------
        from_name : str
            'from_name' child.
        new_name : str
            'new_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['from_name', 'new_name']

    from_name: from_name_cls = from_name_cls
    """
    from_name argument of copy.
    """
    new_name: new_name_cls = new_name_cls
    """
    new_name argument of copy.
    """
