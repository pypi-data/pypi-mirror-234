#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .energy import energy as energy_cls
from .multiphase import multiphase as multiphase_cls
from .viscous import viscous as viscous_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['energy', 'multiphase', 'viscous']

    energy: energy_cls = energy_cls
    """
    energy child of models.
    """
    multiphase: multiphase_cls = multiphase_cls
    """
    multiphase child of models.
    """
    viscous: viscous_cls = viscous_cls
    """
    viscous child of models.
    """
