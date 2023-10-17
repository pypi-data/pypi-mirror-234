#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display_3 import display as display_cls
from .history_filename import history_filename as history_filename_cls
from .report_default_variables import report_default_variables as report_default_variables_cls
from .track_single_particle_stream_1 import track_single_particle_stream as track_single_particle_stream_cls
from .arrow_scale_1 import arrow_scale as arrow_scale_cls
from .arrow_space_1 import arrow_space as arrow_space_cls
from .coarsen_factor import coarsen_factor as coarsen_factor_cls
from .line_width_1 import line_width as line_width_cls
class particle_tracks(Group):
    """
    'particle_tracks' child.
    """

    fluent_name = "particle-tracks"

    child_names = \
        ['display', 'history_filename', 'report_default_variables',
         'track_single_particle_stream', 'arrow_scale', 'arrow_space',
         'coarsen_factor', 'line_width']

    display: display_cls = display_cls
    """
    display child of particle_tracks.
    """
    history_filename: history_filename_cls = history_filename_cls
    """
    history_filename child of particle_tracks.
    """
    report_default_variables: report_default_variables_cls = report_default_variables_cls
    """
    report_default_variables child of particle_tracks.
    """
    track_single_particle_stream: track_single_particle_stream_cls = track_single_particle_stream_cls
    """
    track_single_particle_stream child of particle_tracks.
    """
    arrow_scale: arrow_scale_cls = arrow_scale_cls
    """
    arrow_scale child of particle_tracks.
    """
    arrow_space: arrow_space_cls = arrow_space_cls
    """
    arrow_space child of particle_tracks.
    """
    coarsen_factor: coarsen_factor_cls = coarsen_factor_cls
    """
    coarsen_factor child of particle_tracks.
    """
    line_width: line_width_cls = line_width_cls
    """
    line_width child of particle_tracks.
    """
