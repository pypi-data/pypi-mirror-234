#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename import filename as filename_cls
class read_views(Command):
    """
    Read views from a view file.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "read-views"

    argument_names = \
        ['filename']

    filename: filename_cls = filename_cls
    """
    filename argument of read_views.
    """
