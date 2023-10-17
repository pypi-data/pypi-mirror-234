#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .macro_filename import macro_filename as macro_filename_cls
class execute_macro(Command):
    """
    Run a previously defined macro.
    
    Parameters
    ----------
        macro_filename : str
            'macro_filename' child.
    
    """

    fluent_name = "execute-macro"

    argument_names = \
        ['macro_filename']

    macro_filename: macro_filename_cls = macro_filename_cls
    """
    macro_filename argument of execute_macro.
    """
