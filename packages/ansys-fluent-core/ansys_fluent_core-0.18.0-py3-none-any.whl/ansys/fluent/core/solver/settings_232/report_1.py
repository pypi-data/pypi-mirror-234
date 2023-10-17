#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .simulation_reports import simulation_reports as simulation_reports_cls
from .discrete_phase_1 import discrete_phase as discrete_phase_cls
from .fluxes import fluxes as fluxes_cls
from .flow import flow as flow_cls
from .modified_setting_options import modified_setting_options as modified_setting_options_cls
from .population_balance import population_balance as population_balance_cls
from .heat_exchange_1 import heat_exchange as heat_exchange_cls
from .system import system as system_cls
from .histogram_1 import histogram as histogram_cls
from .aero_optical_distortions import aero_optical_distortions as aero_optical_distortions_cls
from .forces import forces as forces_cls
from .mphase_summary import mphase_summary as mphase_summary_cls
from .particle_summary import particle_summary as particle_summary_cls
from .path_line_summary import path_line_summary as path_line_summary_cls
from .projected_surface_area import projected_surface_area as projected_surface_area_cls
from .summary_1 import summary as summary_cls
from .surface_integrals import surface_integrals as surface_integrals_cls
from .volume_integrals import volume_integrals as volume_integrals_cls
class report(Group):
    """
    'report' child.
    """

    fluent_name = "report"

    child_names = \
        ['simulation_reports', 'discrete_phase', 'fluxes', 'flow',
         'modified_setting_options', 'population_balance', 'heat_exchange',
         'system', 'histogram']

    simulation_reports: simulation_reports_cls = simulation_reports_cls
    """
    simulation_reports child of report.
    """
    discrete_phase: discrete_phase_cls = discrete_phase_cls
    """
    discrete_phase child of report.
    """
    fluxes: fluxes_cls = fluxes_cls
    """
    fluxes child of report.
    """
    flow: flow_cls = flow_cls
    """
    flow child of report.
    """
    modified_setting_options: modified_setting_options_cls = modified_setting_options_cls
    """
    modified_setting_options child of report.
    """
    population_balance: population_balance_cls = population_balance_cls
    """
    population_balance child of report.
    """
    heat_exchange: heat_exchange_cls = heat_exchange_cls
    """
    heat_exchange child of report.
    """
    system: system_cls = system_cls
    """
    system child of report.
    """
    histogram: histogram_cls = histogram_cls
    """
    histogram child of report.
    """
    command_names = \
        ['aero_optical_distortions', 'forces', 'mphase_summary',
         'particle_summary', 'path_line_summary', 'projected_surface_area',
         'summary', 'surface_integrals', 'volume_integrals']

    aero_optical_distortions: aero_optical_distortions_cls = aero_optical_distortions_cls
    """
    aero_optical_distortions command of report.
    """
    forces: forces_cls = forces_cls
    """
    forces command of report.
    """
    mphase_summary: mphase_summary_cls = mphase_summary_cls
    """
    mphase_summary command of report.
    """
    particle_summary: particle_summary_cls = particle_summary_cls
    """
    particle_summary command of report.
    """
    path_line_summary: path_line_summary_cls = path_line_summary_cls
    """
    path_line_summary command of report.
    """
    projected_surface_area: projected_surface_area_cls = projected_surface_area_cls
    """
    projected_surface_area command of report.
    """
    summary: summary_cls = summary_cls
    """
    summary command of report.
    """
    surface_integrals: surface_integrals_cls = surface_integrals_cls
    """
    surface_integrals command of report.
    """
    volume_integrals: volume_integrals_cls = volume_integrals_cls
    """
    volume_integrals command of report.
    """
