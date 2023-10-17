#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .data_sampling import data_sampling as data_sampling_cls
from .sampling_interval import sampling_interval as sampling_interval_cls
from .statistics_shear_stress import statistics_shear_stress as statistics_shear_stress_cls
from .statistics_heat_flux import statistics_heat_flux as statistics_heat_flux_cls
from .wall_statistics import wall_statistics as wall_statistics_cls
from .force_statistics import force_statistics as force_statistics_cls
from .time_statistics_dpm import time_statistics_dpm as time_statistics_dpm_cls
from .species_list import species_list as species_list_cls
from .statistics_mixture_fraction import statistics_mixture_fraction as statistics_mixture_fraction_cls
from .statistics_reaction_progress import statistics_reaction_progress as statistics_reaction_progress_cls
from .save_cff_unsteady_statistics import save_cff_unsteady_statistics as save_cff_unsteady_statistics_cls
from .udf_cf_names import udf_cf_names as udf_cf_names_cls
class data_sampling(Group):
    """
    'data_sampling' child.
    """

    fluent_name = "data-sampling"

    child_names = \
        ['data_sampling', 'sampling_interval', 'statistics_shear_stress',
         'statistics_heat_flux', 'wall_statistics', 'force_statistics',
         'time_statistics_dpm', 'species_list', 'statistics_mixture_fraction',
         'statistics_reaction_progress', 'save_cff_unsteady_statistics',
         'udf_cf_names']

    data_sampling: data_sampling_cls = data_sampling_cls
    """
    data_sampling child of data_sampling.
    """
    sampling_interval: sampling_interval_cls = sampling_interval_cls
    """
    sampling_interval child of data_sampling.
    """
    statistics_shear_stress: statistics_shear_stress_cls = statistics_shear_stress_cls
    """
    statistics_shear_stress child of data_sampling.
    """
    statistics_heat_flux: statistics_heat_flux_cls = statistics_heat_flux_cls
    """
    statistics_heat_flux child of data_sampling.
    """
    wall_statistics: wall_statistics_cls = wall_statistics_cls
    """
    wall_statistics child of data_sampling.
    """
    force_statistics: force_statistics_cls = force_statistics_cls
    """
    force_statistics child of data_sampling.
    """
    time_statistics_dpm: time_statistics_dpm_cls = time_statistics_dpm_cls
    """
    time_statistics_dpm child of data_sampling.
    """
    species_list: species_list_cls = species_list_cls
    """
    species_list child of data_sampling.
    """
    statistics_mixture_fraction: statistics_mixture_fraction_cls = statistics_mixture_fraction_cls
    """
    statistics_mixture_fraction child of data_sampling.
    """
    statistics_reaction_progress: statistics_reaction_progress_cls = statistics_reaction_progress_cls
    """
    statistics_reaction_progress child of data_sampling.
    """
    save_cff_unsteady_statistics: save_cff_unsteady_statistics_cls = save_cff_unsteady_statistics_cls
    """
    save_cff_unsteady_statistics child of data_sampling.
    """
    udf_cf_names: udf_cf_names_cls = udf_cf_names_cls
    """
    udf_cf_names child of data_sampling.
    """
