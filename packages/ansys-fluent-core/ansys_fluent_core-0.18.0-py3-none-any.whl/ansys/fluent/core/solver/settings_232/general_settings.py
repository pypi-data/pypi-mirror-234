#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .contour_plotting_option import contour_plotting_option as contour_plotting_option_cls
from .interaction import interaction as interaction_cls
from .unsteady_tracking import unsteady_tracking as unsteady_tracking_cls
class general_settings(Group):
    """
    Main menu to allow users to set options controlling:
    
     - the optional generation of averaged dpm variables on the fluid mesh to be used for post-processing,
     - the interaction between the discrete particles and their carrier phase,
     - the handling of unsteady particles.
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "general-settings"

    child_names = \
        ['contour_plotting_option', 'interaction', 'unsteady_tracking']

    contour_plotting_option: contour_plotting_option_cls = contour_plotting_option_cls
    """
    contour_plotting_option child of general_settings.
    """
    interaction: interaction_cls = interaction_cls
    """
    interaction child of general_settings.
    """
    unsteady_tracking: unsteady_tracking_cls = unsteady_tracking_cls
    """
    unsteady_tracking child of general_settings.
    """
