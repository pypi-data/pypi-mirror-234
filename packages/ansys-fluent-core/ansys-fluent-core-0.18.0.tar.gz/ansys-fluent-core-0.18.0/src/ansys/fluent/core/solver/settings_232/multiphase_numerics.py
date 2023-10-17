#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .porous_media import porous_media as porous_media_cls
from .compressible_flow import compressible_flow as compressible_flow_cls
from .boiling_parameters import boiling_parameters as boiling_parameters_cls
from .viscous_flow import viscous_flow as viscous_flow_cls
from .heat_mass_transfer import heat_mass_transfer as heat_mass_transfer_cls
from .advanced_stability_controls import advanced_stability_controls as advanced_stability_controls_cls
from .default_controls import default_controls as default_controls_cls
from .face_pressure_controls import face_pressure_controls as face_pressure_controls_cls
from .solution_stabilization import solution_stabilization as solution_stabilization_cls
class multiphase_numerics(Group):
    """
    Enter the multiphase numerics options menu.
    """

    fluent_name = "multiphase-numerics"

    child_names = \
        ['porous_media', 'compressible_flow', 'boiling_parameters',
         'viscous_flow', 'heat_mass_transfer', 'advanced_stability_controls',
         'default_controls', 'face_pressure_controls',
         'solution_stabilization']

    porous_media: porous_media_cls = porous_media_cls
    """
    porous_media child of multiphase_numerics.
    """
    compressible_flow: compressible_flow_cls = compressible_flow_cls
    """
    compressible_flow child of multiphase_numerics.
    """
    boiling_parameters: boiling_parameters_cls = boiling_parameters_cls
    """
    boiling_parameters child of multiphase_numerics.
    """
    viscous_flow: viscous_flow_cls = viscous_flow_cls
    """
    viscous_flow child of multiphase_numerics.
    """
    heat_mass_transfer: heat_mass_transfer_cls = heat_mass_transfer_cls
    """
    heat_mass_transfer child of multiphase_numerics.
    """
    advanced_stability_controls: advanced_stability_controls_cls = advanced_stability_controls_cls
    """
    advanced_stability_controls child of multiphase_numerics.
    """
    default_controls: default_controls_cls = default_controls_cls
    """
    default_controls child of multiphase_numerics.
    """
    face_pressure_controls: face_pressure_controls_cls = face_pressure_controls_cls
    """
    face_pressure_controls child of multiphase_numerics.
    """
    solution_stabilization: solution_stabilization_cls = solution_stabilization_cls
    """
    solution_stabilization child of multiphase_numerics.
    """
