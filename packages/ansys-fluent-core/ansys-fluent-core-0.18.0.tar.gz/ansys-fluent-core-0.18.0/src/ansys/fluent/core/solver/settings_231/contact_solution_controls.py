#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solution_stabilization import solution_stabilization as solution_stabilization_cls
from .verbosity_4 import verbosity as verbosity_cls
from .parameters_1 import parameters as parameters_cls
from .spatial import spatial as spatial_cls
from .transient import transient as transient_cls
from .amg import amg as amg_cls
from .models_2 import models as models_cls
from .methods import methods as methods_cls
from .miscellaneous import miscellaneous as miscellaneous_cls
from .set_settings_to_default import set_settings_to_default as set_settings_to_default_cls
class contact_solution_controls(Group):
    """
    Solver controls for contact marks method.
    """

    fluent_name = "contact-solution-controls"

    child_names = \
        ['solution_stabilization', 'verbosity', 'parameters', 'spatial',
         'transient', 'amg', 'models', 'methods', 'miscellaneous']

    solution_stabilization: solution_stabilization_cls = solution_stabilization_cls
    """
    solution_stabilization child of contact_solution_controls.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of contact_solution_controls.
    """
    parameters: parameters_cls = parameters_cls
    """
    parameters child of contact_solution_controls.
    """
    spatial: spatial_cls = spatial_cls
    """
    spatial child of contact_solution_controls.
    """
    transient: transient_cls = transient_cls
    """
    transient child of contact_solution_controls.
    """
    amg: amg_cls = amg_cls
    """
    amg child of contact_solution_controls.
    """
    models: models_cls = models_cls
    """
    models child of contact_solution_controls.
    """
    methods: methods_cls = methods_cls
    """
    methods child of contact_solution_controls.
    """
    miscellaneous: miscellaneous_cls = miscellaneous_cls
    """
    miscellaneous child of contact_solution_controls.
    """
    command_names = \
        ['set_settings_to_default']

    set_settings_to_default: set_settings_to_default_cls = set_settings_to_default_cls
    """
    set_settings_to_default command of contact_solution_controls.
    """
