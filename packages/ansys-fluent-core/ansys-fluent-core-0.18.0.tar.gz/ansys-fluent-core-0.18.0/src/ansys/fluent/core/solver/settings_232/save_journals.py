#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .separate_journals import separate_journals as separate_journals_cls
class save_journals(Command):
    """
    Save Journals.
    
    Parameters
    ----------
        separate_journals : bool
            'separate_journals' child.
    
    """

    fluent_name = "save-journals"

    argument_names = \
        ['separate_journals']

    separate_journals: separate_journals_cls = separate_journals_cls
    """
    separate_journals argument of save_journals.
    """
