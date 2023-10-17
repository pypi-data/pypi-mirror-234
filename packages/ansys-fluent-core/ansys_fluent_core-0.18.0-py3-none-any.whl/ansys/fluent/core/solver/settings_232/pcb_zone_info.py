#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .ecad_name import ecad_name as ecad_name_cls
from .choice import choice as choice_cls
from .rows import rows as rows_cls
from .columns import columns as columns_cls
from .ref_frame import ref_frame as ref_frame_cls
from .pwr_names import pwr_names as pwr_names_cls
class pcb_zone_info(Group):
    """
    'pcb_zone_info' child.
    """

    fluent_name = "pcb-zone-info"

    child_names = \
        ['ecad_name', 'choice', 'rows', 'columns', 'ref_frame', 'pwr_names']

    ecad_name: ecad_name_cls = ecad_name_cls
    """
    ecad_name child of pcb_zone_info.
    """
    choice: choice_cls = choice_cls
    """
    choice child of pcb_zone_info.
    """
    rows: rows_cls = rows_cls
    """
    rows child of pcb_zone_info.
    """
    columns: columns_cls = columns_cls
    """
    columns child of pcb_zone_info.
    """
    ref_frame: ref_frame_cls = ref_frame_cls
    """
    ref_frame child of pcb_zone_info.
    """
    pwr_names: pwr_names_cls = pwr_names_cls
    """
    pwr_names child of pcb_zone_info.
    """
