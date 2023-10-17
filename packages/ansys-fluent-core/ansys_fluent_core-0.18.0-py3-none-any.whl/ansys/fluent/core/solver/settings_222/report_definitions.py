#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mesh import mesh as mesh_cls
from .surface import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .flux import flux as flux_cls
from .injection import injection as injection_cls
from .user_defined import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .expression import expression as expression_cls
from .custom import custom as custom_cls
from .compute_2 import compute as compute_cls
class report_definitions(Group):
    """
    'report_definitions' child.
    """

    fluent_name = "report-definitions"

    child_names = \
        ['mesh', 'surface', 'volume', 'force', 'lift', 'drag', 'moment',
         'flux', 'injection', 'user_defined', 'aeromechanics', 'expression',
         'custom']

    mesh: mesh_cls = mesh_cls
    """
    mesh child of report_definitions.
    """
    surface: surface_cls = surface_cls
    """
    surface child of report_definitions.
    """
    volume: volume_cls = volume_cls
    """
    volume child of report_definitions.
    """
    force: force_cls = force_cls
    """
    force child of report_definitions.
    """
    lift: lift_cls = lift_cls
    """
    lift child of report_definitions.
    """
    drag: drag_cls = drag_cls
    """
    drag child of report_definitions.
    """
    moment: moment_cls = moment_cls
    """
    moment child of report_definitions.
    """
    flux: flux_cls = flux_cls
    """
    flux child of report_definitions.
    """
    injection: injection_cls = injection_cls
    """
    injection child of report_definitions.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of report_definitions.
    """
    aeromechanics: aeromechanics_cls = aeromechanics_cls
    """
    aeromechanics child of report_definitions.
    """
    expression: expression_cls = expression_cls
    """
    expression child of report_definitions.
    """
    custom: custom_cls = custom_cls
    """
    custom child of report_definitions.
    """
    command_names = \
        ['compute']

    compute: compute_cls = compute_cls
    """
    compute command of report_definitions.
    """
