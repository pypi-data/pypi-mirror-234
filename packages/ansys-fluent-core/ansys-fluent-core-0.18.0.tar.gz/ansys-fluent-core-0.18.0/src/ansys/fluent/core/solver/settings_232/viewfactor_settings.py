#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .basis import basis as basis_cls
from .method_1 import method as method_cls
from .surfaces_2 import surfaces as surfaces_cls
from .smoothing import smoothing as smoothing_cls
from .resolution import resolution as resolution_cls
from .separation import separation as separation_cls
from .subdivide import subdivide as subdivide_cls
from .non_participating_zone_temperature import non_participating_zone_temperature as non_participating_zone_temperature_cls
class viewfactor_settings(Group):
    """
    Enter viewfactor related settings.
    """

    fluent_name = "viewfactor-settings"

    child_names = \
        ['basis', 'method', 'surfaces', 'smoothing', 'resolution',
         'separation', 'subdivide', 'non_participating_zone_temperature']

    basis: basis_cls = basis_cls
    """
    basis child of viewfactor_settings.
    """
    method: method_cls = method_cls
    """
    method child of viewfactor_settings.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of viewfactor_settings.
    """
    smoothing: smoothing_cls = smoothing_cls
    """
    smoothing child of viewfactor_settings.
    """
    resolution: resolution_cls = resolution_cls
    """
    resolution child of viewfactor_settings.
    """
    separation: separation_cls = separation_cls
    """
    separation child of viewfactor_settings.
    """
    subdivide: subdivide_cls = subdivide_cls
    """
    subdivide child of viewfactor_settings.
    """
    non_participating_zone_temperature: non_participating_zone_temperature_cls = non_participating_zone_temperature_cls
    """
    non_participating_zone_temperature child of viewfactor_settings.
    """
