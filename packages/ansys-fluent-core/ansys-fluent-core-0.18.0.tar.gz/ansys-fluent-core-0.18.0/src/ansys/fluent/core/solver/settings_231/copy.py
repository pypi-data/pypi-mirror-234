#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .orig_beam_name import orig_beam_name as orig_beam_name_cls
from .beam_name import beam_name as beam_name_cls
from .ap_face_zone import ap_face_zone as ap_face_zone_cls
from .beam_length import beam_length as beam_length_cls
from .ray_npoints import ray_npoints as ray_npoints_cls
from .x_beam_vector import x_beam_vector as x_beam_vector_cls
from .y_beam_vector import y_beam_vector as y_beam_vector_cls
from .z_beam_vector import z_beam_vector as z_beam_vector_cls
class copy(Command):
    """
    Copy optical beam grid.
    
    Parameters
    ----------
        orig_beam_name : str
            Choose the name for the optical beam to be copied.
        beam_name : str
            Set a unique name for each optical beam.
        ap_face_zone : str
            Set the wall face zones to specify the optical aperture surface.
        beam_length : real
            Set the length of optical beam propagation.
        ray_npoints : int
            Set the number of grid point in each ray of the optical beam.
        x_beam_vector : real
            Set the x-component of the beam propagation vector.
        y_beam_vector : real
            Set the y-component of the beam propagation vector.
        z_beam_vector : real
            Set the z-component of the beam propagation vector.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['orig_beam_name', 'beam_name', 'ap_face_zone', 'beam_length',
         'ray_npoints', 'x_beam_vector', 'y_beam_vector', 'z_beam_vector']

    orig_beam_name: orig_beam_name_cls = orig_beam_name_cls
    """
    orig_beam_name argument of copy.
    """
    beam_name: beam_name_cls = beam_name_cls
    """
    beam_name argument of copy.
    """
    ap_face_zone: ap_face_zone_cls = ap_face_zone_cls
    """
    ap_face_zone argument of copy.
    """
    beam_length: beam_length_cls = beam_length_cls
    """
    beam_length argument of copy.
    """
    ray_npoints: ray_npoints_cls = ray_npoints_cls
    """
    ray_npoints argument of copy.
    """
    x_beam_vector: x_beam_vector_cls = x_beam_vector_cls
    """
    x_beam_vector argument of copy.
    """
    y_beam_vector: y_beam_vector_cls = y_beam_vector_cls
    """
    y_beam_vector argument of copy.
    """
    z_beam_vector: z_beam_vector_cls = z_beam_vector_cls
    """
    z_beam_vector argument of copy.
    """
