#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .si_delete import si_delete as si_delete_cls
class delete(Command):
    """
    Delete a mesh interface.
    
    Parameters
    ----------
        si_delete : str
            'si_delete' child.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['si_delete']

    si_delete: si_delete_cls = si_delete_cls
    """
    si_delete argument of delete.
    """
