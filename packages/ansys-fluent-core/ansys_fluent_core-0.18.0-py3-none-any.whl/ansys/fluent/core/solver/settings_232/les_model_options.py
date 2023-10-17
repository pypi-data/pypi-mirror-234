#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .dynamic_stress import dynamic_stress as dynamic_stress_cls
from .dynamic_energy_flux import dynamic_energy_flux as dynamic_energy_flux_cls
from .dynamic_scalar_flux import dynamic_scalar_flux as dynamic_scalar_flux_cls
from .subgrid_dynamic_fvar import subgrid_dynamic_fvar as subgrid_dynamic_fvar_cls
from .cvreman import cvreman as cvreman_cls
from .csigma import csigma as csigma_cls
from .wall_model import wall_model as wall_model_cls
from .cw1 import cw1 as cw1_cls
from .cw2 import cw2 as cw2_cls
class les_model_options(Group):
    """
    'les_model_options' child.
    """

    fluent_name = "les-model-options"

    child_names = \
        ['dynamic_stress', 'dynamic_energy_flux', 'dynamic_scalar_flux',
         'subgrid_dynamic_fvar', 'cvreman', 'csigma', 'wall_model', 'cw1',
         'cw2']

    dynamic_stress: dynamic_stress_cls = dynamic_stress_cls
    """
    dynamic_stress child of les_model_options.
    """
    dynamic_energy_flux: dynamic_energy_flux_cls = dynamic_energy_flux_cls
    """
    dynamic_energy_flux child of les_model_options.
    """
    dynamic_scalar_flux: dynamic_scalar_flux_cls = dynamic_scalar_flux_cls
    """
    dynamic_scalar_flux child of les_model_options.
    """
    subgrid_dynamic_fvar: subgrid_dynamic_fvar_cls = subgrid_dynamic_fvar_cls
    """
    subgrid_dynamic_fvar child of les_model_options.
    """
    cvreman: cvreman_cls = cvreman_cls
    """
    cvreman child of les_model_options.
    """
    csigma: csigma_cls = csigma_cls
    """
    csigma child of les_model_options.
    """
    wall_model: wall_model_cls = wall_model_cls
    """
    wall_model child of les_model_options.
    """
    cw1: cw1_cls = cw1_cls
    """
    cw1 child of les_model_options.
    """
    cw2: cw2_cls = cw2_cls
    """
    cw2 child of les_model_options.
    """
