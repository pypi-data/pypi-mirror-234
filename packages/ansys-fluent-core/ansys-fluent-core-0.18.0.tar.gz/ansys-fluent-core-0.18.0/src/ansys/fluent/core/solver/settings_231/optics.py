#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_3 import enable as enable_cls
from .beams import beams as beams_cls
from .statistics import statistics as statistics_cls
from .sampling_iterations import sampling_iterations as sampling_iterations_cls
from .index_of_refraction import index_of_refraction as index_of_refraction_cls
from .report import report as report_cls
from .verbosity_2 import verbosity as verbosity_cls
class optics(Group):
    """
    Enter the optics model menu.
    """

    fluent_name = "optics"

    child_names = \
        ['enable', 'beams', 'statistics', 'sampling_iterations',
         'index_of_refraction', 'report', 'verbosity']

    enable: enable_cls = enable_cls
    """
    enable child of optics.
    """
    beams: beams_cls = beams_cls
    """
    beams child of optics.
    """
    statistics: statistics_cls = statistics_cls
    """
    statistics child of optics.
    """
    sampling_iterations: sampling_iterations_cls = sampling_iterations_cls
    """
    sampling_iterations child of optics.
    """
    index_of_refraction: index_of_refraction_cls = index_of_refraction_cls
    """
    index_of_refraction child of optics.
    """
    report: report_cls = report_cls
    """
    report child of optics.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of optics.
    """
