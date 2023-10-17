#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pseudo_transient import pseudo_transient as pseudo_transient_cls
from .p_v_coupling import p_v_coupling as p_v_coupling_cls
from .hybrid_nita import hybrid_nita as hybrid_nita_cls
from .equation_order import equation_order as equation_order_cls
from .anti_diffusion import anti_diffusion as anti_diffusion_cls
class advanced_stability_controls(Group):
    """
    'advanced_stability_controls' child.
    """

    fluent_name = "advanced-stability-controls"

    child_names = \
        ['pseudo_transient', 'p_v_coupling', 'hybrid_nita', 'equation_order',
         'anti_diffusion']

    pseudo_transient: pseudo_transient_cls = pseudo_transient_cls
    """
    pseudo_transient child of advanced_stability_controls.
    """
    p_v_coupling: p_v_coupling_cls = p_v_coupling_cls
    """
    p_v_coupling child of advanced_stability_controls.
    """
    hybrid_nita: hybrid_nita_cls = hybrid_nita_cls
    """
    hybrid_nita child of advanced_stability_controls.
    """
    equation_order: equation_order_cls = equation_order_cls
    """
    equation_order child of advanced_stability_controls.
    """
    anti_diffusion: anti_diffusion_cls = anti_diffusion_cls
    """
    anti_diffusion child of advanced_stability_controls.
    """
