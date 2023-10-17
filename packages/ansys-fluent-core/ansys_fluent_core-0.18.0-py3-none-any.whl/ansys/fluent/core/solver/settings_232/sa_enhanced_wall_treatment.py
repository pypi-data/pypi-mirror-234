#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

class sa_enhanced_wall_treatment(Boolean):
    """
    Enable/disable the enhanced wall treatment for the Spalart-Allmaras model.
    If disabled, no smooth blending between the viscous sublayer and the
    log-law formulation is employed, as was done in versions previous to Fluent14.
    """

    fluent_name = "sa-enhanced-wall-treatment?"

