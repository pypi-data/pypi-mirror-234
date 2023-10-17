#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .implicit_bodyforce_treatment import implicit_bodyforce_treatment as implicit_bodyforce_treatment_cls
from .velocity_formulation import velocity_formulation as velocity_formulation_cls
from .physical_velocity_formulation import physical_velocity_formulation as physical_velocity_formulation_cls
from .disable_rhie_chow_flux import disable_rhie_chow_flux as disable_rhie_chow_flux_cls
from .presto_pressure_scheme import presto_pressure_scheme as presto_pressure_scheme_cls
from .first_to_second_order_blending_1 import first_to_second_order_blending as first_to_second_order_blending_cls
from .alternate_diffusion_for_porous_region_solids import alternate_diffusion_for_porous_region_solids as alternate_diffusion_for_porous_region_solids_cls
class numerics_pbns(Group):
    """
    Set numeric options.
    """

    fluent_name = "numerics-pbns"

    child_names = \
        ['implicit_bodyforce_treatment', 'velocity_formulation',
         'physical_velocity_formulation', 'disable_rhie_chow_flux',
         'presto_pressure_scheme', 'first_to_second_order_blending',
         'alternate_diffusion_for_porous_region_solids']

    implicit_bodyforce_treatment: implicit_bodyforce_treatment_cls = implicit_bodyforce_treatment_cls
    """
    implicit_bodyforce_treatment child of numerics_pbns.
    """
    velocity_formulation: velocity_formulation_cls = velocity_formulation_cls
    """
    velocity_formulation child of numerics_pbns.
    """
    physical_velocity_formulation: physical_velocity_formulation_cls = physical_velocity_formulation_cls
    """
    physical_velocity_formulation child of numerics_pbns.
    """
    disable_rhie_chow_flux: disable_rhie_chow_flux_cls = disable_rhie_chow_flux_cls
    """
    disable_rhie_chow_flux child of numerics_pbns.
    """
    presto_pressure_scheme: presto_pressure_scheme_cls = presto_pressure_scheme_cls
    """
    presto_pressure_scheme child of numerics_pbns.
    """
    first_to_second_order_blending: first_to_second_order_blending_cls = first_to_second_order_blending_cls
    """
    first_to_second_order_blending child of numerics_pbns.
    """
    alternate_diffusion_for_porous_region_solids: alternate_diffusion_for_porous_region_solids_cls = alternate_diffusion_for_porous_region_solids_cls
    """
    alternate_diffusion_for_porous_region_solids child of numerics_pbns.
    """
