#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class beams:
    fluent_name = ...
    command_names = ...

    def copy(self, orig_beam_name: str, beam_name: str, ap_face_zone: str, beam_length: Union[float, str], ray_npoints: int, x_beam_vector: Union[float, str], y_beam_vector: Union[float, str], z_beam_vector: Union[float, str]):
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

    def list_beam_parameters(self, beam_name: str):
        """
        List parameters of optical beam grid.
        
        Parameters
        ----------
            beam_name : str
                Choose the name for the optical beam to be listed.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
