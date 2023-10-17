#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_volumetric_reactions import enable_volumetric_reactions as enable_volumetric_reactions_cls
from .enable_wall_surface import enable_wall_surface as enable_wall_surface_cls
from .enable_particle_surface import enable_particle_surface as enable_particle_surface_cls
from .enable_electrochemical_surface import enable_electrochemical_surface as enable_electrochemical_surface_cls
class reactions(Group):
    """
    'reactions' child.
    """

    fluent_name = "reactions"

    child_names = \
        ['enable_volumetric_reactions', 'enable_wall_surface',
         'enable_particle_surface', 'enable_electrochemical_surface']

    enable_volumetric_reactions: enable_volumetric_reactions_cls = enable_volumetric_reactions_cls
    """
    enable_volumetric_reactions child of reactions.
    """
    enable_wall_surface: enable_wall_surface_cls = enable_wall_surface_cls
    """
    enable_wall_surface child of reactions.
    """
    enable_particle_surface: enable_particle_surface_cls = enable_particle_surface_cls
    """
    enable_particle_surface child of reactions.
    """
    enable_electrochemical_surface: enable_electrochemical_surface_cls = enable_electrochemical_surface_cls
    """
    enable_electrochemical_surface child of reactions.
    """
