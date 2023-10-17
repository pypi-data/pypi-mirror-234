#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .c1 import c1 as c1_cls
from .c2 import c2 as c2_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .effective_temperature import effective_temperature as effective_temperature_cls
class sutherland(Group):
    """
    'sutherland' child.
    """

    fluent_name = "sutherland"

    child_names = \
        ['option', 'c1', 'c2', 'reference_viscosity', 'reference_temperature',
         'effective_temperature']

    option: option_cls = option_cls
    """
    option child of sutherland.
    """
    c1: c1_cls = c1_cls
    """
    c1 child of sutherland.
    """
    c2: c2_cls = c2_cls
    """
    c2 child of sutherland.
    """
    reference_viscosity: reference_viscosity_cls = reference_viscosity_cls
    """
    reference_viscosity child of sutherland.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of sutherland.
    """
    effective_temperature: effective_temperature_cls = effective_temperature_cls
    """
    effective_temperature child of sutherland.
    """
