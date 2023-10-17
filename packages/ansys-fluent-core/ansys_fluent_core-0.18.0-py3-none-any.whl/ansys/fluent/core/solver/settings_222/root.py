#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file import file as file_cls
from .setup import setup as setup_cls
from .solution import solution as solution_cls
from .results import results as results_cls
from .parametric_studies import parametric_studies as parametric_studies_cls
from .current_parametric_study import current_parametric_study as current_parametric_study_cls
class root(Group):
    """
    'root' object.
    """

    fluent_name = ""

    child_names = \
        ['file', 'setup', 'solution', 'results', 'parametric_studies',
         'current_parametric_study']

    file: file_cls = file_cls
    """
    file child of root.
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
