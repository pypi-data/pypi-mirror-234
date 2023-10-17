#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .create_zones_from_ccl import create_zones_from_ccl as create_zones_from_ccl_cls
from .read import read as read_cls
from .chemkin_report_each_line import chemkin_report_each_line as chemkin_report_each_line_cls
from .import_fmu import import_fmu as import_fmu_cls
class import_(Group):
    """
    'import' child.
    """

    fluent_name = "import"

    child_names = \
        ['create_zones_from_ccl']

    create_zones_from_ccl: create_zones_from_ccl_cls = create_zones_from_ccl_cls
    """
    create_zones_from_ccl child of import_.
    """
    command_names = \
        ['read', 'chemkin_report_each_line', 'import_fmu']

    read: read_cls = read_cls
    """
    read command of import_.
    """
    chemkin_report_each_line: chemkin_report_each_line_cls = chemkin_report_each_line_cls
    """
    chemkin_report_each_line command of import_.
    """
    import_fmu: import_fmu_cls = import_fmu_cls
    """
    import_fmu command of import_.
    """
