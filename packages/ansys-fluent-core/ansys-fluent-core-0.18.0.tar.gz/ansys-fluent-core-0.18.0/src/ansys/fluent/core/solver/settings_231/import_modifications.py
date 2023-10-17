#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename import filename as filename_cls
class import_modifications(Command):
    """
    Import a list of case modifications from a tsv file.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "import-modifications"

    argument_names = \
        ['filename']

    filename: filename_cls = filename_cls
    """
    filename argument of import_modifications.
    """
