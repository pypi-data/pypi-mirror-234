#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_1 import type as type_cls
from .formula import formula as formula_cls
class copy_database_material_by_formula(Command):
    """
    'copy_database_material_by_formula' command.
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
    
    """

    fluent_name = "copy-database-material-by-formula"

    argument_names = \
        ['type', 'formula']

    type: type_cls = type_cls
    """
    type argument of copy_database_material_by_formula.
    """
    formula: formula_cls = formula_cls
    """
    formula argument of copy_database_material_by_formula.
    """
