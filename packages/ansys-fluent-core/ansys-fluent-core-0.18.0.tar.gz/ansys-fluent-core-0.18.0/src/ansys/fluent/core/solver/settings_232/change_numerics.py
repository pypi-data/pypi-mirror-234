#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_sided_area_vector import use_sided_area_vector as use_sided_area_vector_cls
from .use_nci_sided_area_vectors import use_nci_sided_area_vectors as use_nci_sided_area_vectors_cls
from .recrete import recrete as recrete_cls
class change_numerics(Command):
    """
    Enable modified non-conformal interface numerics.
    
    Parameters
    ----------
        use_sided_area_vector : bool
            'use_sided_area_vector' child.
        use_nci_sided_area_vectors : bool
            'use_nci_sided_area_vectors' child.
        recrete : bool
            'recrete' child.
    
    """

    fluent_name = "change-numerics?"

    argument_names = \
        ['use_sided_area_vector', 'use_nci_sided_area_vectors', 'recrete']

    use_sided_area_vector: use_sided_area_vector_cls = use_sided_area_vector_cls
    """
    use_sided_area_vector argument of change_numerics.
    """
    use_nci_sided_area_vectors: use_nci_sided_area_vectors_cls = use_nci_sided_area_vectors_cls
    """
    use_nci_sided_area_vectors argument of change_numerics.
    """
    recrete: recrete_cls = recrete_cls
    """
    recrete argument of change_numerics.
    """
