#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename import filename as filename_cls
class define_macro(Command):
    """
    Save input to a named macro.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "define-macro"

    argument_names = \
        ['filename']

    filename: filename_cls = filename_cls
    """
    filename argument of define_macro.
    """
