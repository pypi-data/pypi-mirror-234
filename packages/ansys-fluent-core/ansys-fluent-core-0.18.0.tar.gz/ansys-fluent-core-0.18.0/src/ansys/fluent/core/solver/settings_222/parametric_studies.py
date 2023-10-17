#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .initialize import initialize as initialize_cls
from .duplicate import duplicate as duplicate_cls
from .set_as_current import set_as_current as set_as_current_cls
from .use_base_data import use_base_data as use_base_data_cls
from .export_design_table import export_design_table as export_design_table_cls
from .import_design_table import import_design_table as import_design_table_cls
from .parametric_studies_child import parametric_studies_child

class parametric_studies(NamedObject[parametric_studies_child], _CreatableNamedObjectMixin[parametric_studies_child]):
    """
    'parametric_studies' child.
    """

    fluent_name = "parametric-studies"

    command_names = \
        ['initialize', 'duplicate', 'set_as_current', 'use_base_data',
         'export_design_table', 'import_design_table']

    initialize: initialize_cls = initialize_cls
    """
    initialize command of parametric_studies.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of parametric_studies.
    """
    set_as_current: set_as_current_cls = set_as_current_cls
    """
    set_as_current command of parametric_studies.
    """
    use_base_data: use_base_data_cls = use_base_data_cls
    """
    use_base_data command of parametric_studies.
    """
    export_design_table: export_design_table_cls = export_design_table_cls
    """
    export_design_table command of parametric_studies.
    """
    import_design_table: import_design_table_cls = import_design_table_cls
    """
    import_design_table command of parametric_studies.
    """
    child_object_type: parametric_studies_child = parametric_studies_child
    """
    child_object_type of parametric_studies.
    """
