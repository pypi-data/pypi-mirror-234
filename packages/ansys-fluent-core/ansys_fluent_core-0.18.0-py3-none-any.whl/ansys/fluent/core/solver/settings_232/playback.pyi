#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class playback:
    fluent_name = ...
    child_names = ...
    set_custom_frames = ...
    video = ...
    command_names = ...

    def read_animation(self, read_from_file: bool, animation_file_name: str, select_from_available: bool, animation_name: str):
        """
        Read new animation from file or already-defined animations.
        
        Parameters
        ----------
            read_from_file : bool
                'read_from_file' child.
            animation_file_name : str
                'animation_file_name' child.
            select_from_available : bool
                'select_from_available' child.
            animation_name : str
                'animation_name' child.
        
        """

    def write_animation(self, format_name: str):
        """
        Write animation sequence to the file.
        
        Parameters
        ----------
            format_name : str
                'format_name' child.
        
        """

    def stored_view(self, view: bool):
        """
        Play the 3D animation sequence using the view stored in the sequence.
        
        Parameters
        ----------
            view : bool
                Yes: "Stored View", no: "Different View".
        
        """

