#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .application import application as application_cls
from .border_3 import border as border_cls
from .bottom_3 import bottom as bottom_cls
from .clear_3 import clear as clear_cls
from .company import company as company_cls
from .date import date as date_cls
from .left_3 import left as left_cls
from .right_4 import right as right_cls
from .top_3 import top as top_cls
from .visible_4 import visible as visible_cls
from .alignment import alignment as alignment_cls
class text(Group):
    """
    Enter the text window options menu.
    """

    fluent_name = "text"

    child_names = \
        ['application', 'border', 'bottom', 'clear', 'company', 'date',
         'left', 'right', 'top', 'visible', 'alignment']

    application: application_cls = application_cls
    """
    application child of text.
    """
    border: border_cls = border_cls
    """
    border child of text.
    """
    bottom: bottom_cls = bottom_cls
    """
    bottom child of text.
    """
    clear: clear_cls = clear_cls
    """
    clear child of text.
    """
    company: company_cls = company_cls
    """
    company child of text.
    """
    date: date_cls = date_cls
    """
    date child of text.
    """
    left: left_cls = left_cls
    """
    left child of text.
    """
    right: right_cls = right_cls
    """
    right child of text.
    """
    top: top_cls = top_cls
    """
    top child of text.
    """
    visible: visible_cls = visible_cls
    """
    visible child of text.
    """
    alignment: alignment_cls = alignment_cls
    """
    alignment child of text.
    """
