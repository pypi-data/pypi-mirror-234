#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .reactions_1 import reactions as reactions_cls
from .reaction_source_term_relaxation_factor import reaction_source_term_relaxation_factor as reaction_source_term_relaxation_factor_cls
from .numerics import numerics as numerics_cls
from .numerics_dbns import numerics_dbns as numerics_dbns_cls
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['reactions', 'reaction_source_term_relaxation_factor', 'numerics',
         'numerics_dbns']

    reactions: reactions_cls = reactions_cls
    """
    reactions child of expert.
    """
    reaction_source_term_relaxation_factor: reaction_source_term_relaxation_factor_cls = reaction_source_term_relaxation_factor_cls
    """
    reaction_source_term_relaxation_factor child of expert.
    """
    numerics: numerics_cls = numerics_cls
    """
    numerics child of expert.
    """
    numerics_dbns: numerics_dbns_cls = numerics_dbns_cls
    """
    numerics_dbns child of expert.
    """
