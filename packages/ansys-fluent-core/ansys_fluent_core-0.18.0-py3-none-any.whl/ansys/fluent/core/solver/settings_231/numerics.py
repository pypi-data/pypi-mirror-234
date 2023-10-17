#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .averaging import averaging as averaging_cls
from .source_terms import source_terms as source_terms_cls
from .tracking import tracking as tracking_cls
class numerics(Group):
    """
    Main menu to allow users to set options controlling the solution of ordinary differential equations describing 
    the underlying physics of the Discrete Phase Model.
    For more details consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "numerics"

    child_names = \
        ['averaging', 'source_terms', 'tracking']

    averaging: averaging_cls = averaging_cls
    """
    averaging child of numerics.
    """
    source_terms: source_terms_cls = source_terms_cls
    """
    source_terms child of numerics.
    """
    tracking: tracking_cls = tracking_cls
    """
    tracking child of numerics.
    """
