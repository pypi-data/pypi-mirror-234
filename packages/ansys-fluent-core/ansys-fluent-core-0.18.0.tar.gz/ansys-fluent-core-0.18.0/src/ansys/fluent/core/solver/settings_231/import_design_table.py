#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filepath import filepath as filepath_cls
from .delete_existing import delete_existing as delete_existing_cls
class import_design_table(Command):
    """
    Import Design Point Table.
    
    Parameters
    ----------
        filepath : str
            'filepath' child.
        delete_existing : bool
            'delete_existing' child.
    
    """

    fluent_name = "import-design-table"

    argument_names = \
        ['filepath', 'delete_existing']

    filepath: filepath_cls = filepath_cls
    """
    filepath argument of import_design_table.
    """
    delete_existing: delete_existing_cls = delete_existing_cls
    """
    delete_existing argument of import_design_table.
    """
