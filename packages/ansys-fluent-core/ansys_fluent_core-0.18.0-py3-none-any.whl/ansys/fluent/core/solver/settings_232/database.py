#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .database_type import database_type as database_type_cls
from .copy_by_formula import copy_by_formula as copy_by_formula_cls
from .copy_by_name import copy_by_name as copy_by_name_cls
from .list_materials import list_materials as list_materials_cls
from .list_properties_2 import list_properties as list_properties_cls
class database(Group):
    """
    'database' child.
    """

    fluent_name = "database"

    child_names = \
        ['database_type']

    database_type: database_type_cls = database_type_cls
    """
    database_type child of database.
    """
    command_names = \
        ['copy_by_formula', 'copy_by_name', 'list_materials',
         'list_properties']

    copy_by_formula: copy_by_formula_cls = copy_by_formula_cls
    """
    copy_by_formula command of database.
    """
    copy_by_name: copy_by_name_cls = copy_by_name_cls
    """
    copy_by_name command of database.
    """
    list_materials: list_materials_cls = list_materials_cls
    """
    list_materials command of database.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of database.
    """
