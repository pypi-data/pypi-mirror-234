#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_2 import type as type_cls
from .formula import formula as formula_cls
class copy_by_formula(Command):
    """
    Copy a material from the database (pick by formula).
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
    
    """

    fluent_name = "copy-by-formula"

    argument_names = \
        ['type', 'formula']

    type: type_cls = type_cls
    """
    type argument of copy_by_formula.
    """
    formula: formula_cls = formula_cls
    """
    formula argument of copy_by_formula.
    """
