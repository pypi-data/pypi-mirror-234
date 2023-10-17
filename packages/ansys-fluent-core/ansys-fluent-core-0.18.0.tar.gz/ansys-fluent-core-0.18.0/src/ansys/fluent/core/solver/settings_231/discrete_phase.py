#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_expert_view import enable_expert_view as enable_expert_view_cls
from .general_settings import general_settings as general_settings_cls
from .injections import injections as injections_cls
from .numerics import numerics as numerics_cls
from .parallel import parallel as parallel_cls
from .physical_models_1 import physical_models as physical_models_cls
from .tracking_1 import tracking as tracking_cls
from .user_defined_functions import user_defined_functions as user_defined_functions_cls
class discrete_phase(Group):
    """
    Toplevel menu of the Discrete Phase multiphase model. A discrete phase model (DPM) is used when the aim is to investigate the behavior of the particles from a Lagrangian view and a discrete perspective.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['enable_expert_view', 'general_settings', 'injections', 'numerics',
         'parallel', 'physical_models', 'tracking', 'user_defined_functions']

    enable_expert_view: enable_expert_view_cls = enable_expert_view_cls
    """
    enable_expert_view child of discrete_phase.
    """
    general_settings: general_settings_cls = general_settings_cls
    """
    general_settings child of discrete_phase.
    """
    injections: injections_cls = injections_cls
    """
    injections child of discrete_phase.
    """
    numerics: numerics_cls = numerics_cls
    """
    numerics child of discrete_phase.
    """
    parallel: parallel_cls = parallel_cls
    """
    parallel child of discrete_phase.
    """
    physical_models: physical_models_cls = physical_models_cls
    """
    physical_models child of discrete_phase.
    """
    tracking: tracking_cls = tracking_cls
    """
    tracking child of discrete_phase.
    """
    user_defined_functions: user_defined_functions_cls = user_defined_functions_cls
    """
    user_defined_functions child of discrete_phase.
    """
