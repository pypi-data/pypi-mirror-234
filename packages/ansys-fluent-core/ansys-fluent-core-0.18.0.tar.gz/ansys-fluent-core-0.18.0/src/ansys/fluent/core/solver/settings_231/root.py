#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file import file as file_cls
from .mesh import mesh as mesh_cls
from .server import server as server_cls
from .setup import setup as setup_cls
from .solution import solution as solution_cls
from .results import results as results_cls
from .parametric_studies import parametric_studies as parametric_studies_cls
from .current_parametric_study import current_parametric_study as current_parametric_study_cls
from .parallel_1 import parallel as parallel_cls
from .report_1 import report as report_cls
from .exit import exit as exit_cls
class root(Group):
    """
    'root' object.
    """

    fluent_name = ""

    child_names = \
        ['file', 'mesh', 'server', 'setup', 'solution', 'results',
         'parametric_studies', 'current_parametric_study', 'parallel',
         'report']

    file: file_cls = file_cls
    """
    file child of root.
    """
    mesh: mesh_cls = mesh_cls
    """
    mesh child of root.
    """
    server: server_cls = server_cls
    """
    server child of root.
    """
    setup: setup_cls = setup_cls
    """
    setup child of root.
    """
    solution: solution_cls = solution_cls
    """
    solution child of root.
    """
    results: results_cls = results_cls
    """
    results child of root.
    """
    parametric_studies: parametric_studies_cls = parametric_studies_cls
    """
    parametric_studies child of root.
    """
    current_parametric_study: current_parametric_study_cls = current_parametric_study_cls
    """
    current_parametric_study child of root.
    """
    parallel: parallel_cls = parallel_cls
    """
    parallel child of root.
    """
    report: report_cls = report_cls
    """
    report child of root.
    """
    command_names = \
        ['exit']

    exit: exit_cls = exit_cls
    """
    exit command of root.
    """
