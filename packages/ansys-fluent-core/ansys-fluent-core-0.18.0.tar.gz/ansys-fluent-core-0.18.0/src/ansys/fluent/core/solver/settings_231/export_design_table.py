#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filepath import filepath as filepath_cls
class export_design_table(Command):
    """
    Export Design Point Table.
    
    Parameters
    ----------
        filepath : str
            'filepath' child.
    
    """

    fluent_name = "export-design-table"

    argument_names = \
        ['filepath']

    filepath: filepath_cls = filepath_cls
    """
    filepath argument of export_design_table.
    """
