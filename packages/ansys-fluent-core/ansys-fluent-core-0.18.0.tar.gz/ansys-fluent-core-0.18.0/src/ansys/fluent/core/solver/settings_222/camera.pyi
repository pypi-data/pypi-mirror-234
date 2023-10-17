#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class camera:
    fluent_name = ...
    command_names = ...

    def dolly(self, right: Union[float, str], up: Union[float, str], in_: Union[float, str]):
        """
        Adjust the camera position and target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
            in_ : real
                'in' child.
        
        """

    def field(self, width: Union[float, str], height: Union[float, str]):
        """
        Set the field of view (width and height).
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        
        """

    def orbit(self, right: Union[float, str], up: Union[float, str]):
        """
        Adjust the camera position without modifying the target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        
        """

    def pan(self, right: Union[float, str], up: Union[float, str]):
        """
        Adjust the camera position without modifying the position.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        
        """

    def position(self, xyz: List[Union[float, str]]):
        """
        Set the camera position.
        
        Parameters
        ----------
            xyz : typing.List[real]
                'xyz' child.
        
        """

    def projection(self, type: str):
        """
        Set the camera projection.
        
        Parameters
        ----------
            type : str
                'type' child.
        
        """

    def roll(self, counter_clockwise: Union[float, str]):
        """
        Adjust the camera up-vector.
        
        Parameters
        ----------
            counter_clockwise : real
                'counter_clockwise' child.
        
        """

    def target(self, xyz: List[Union[float, str]]):
        """
        Set the point to be the center of the camera view.
        
        Parameters
        ----------
            xyz : typing.List[real]
                'xyz' child.
        
        """

    def up_vector(self, xyz: List[Union[float, str]]):
        """
        Set the camera up-vector.
        
        Parameters
        ----------
            xyz : typing.List[real]
                'xyz' child.
        
        """

    def zoom(self, factor: Union[float, str]):
        """
        Adjust the camera field of view.
        
        Parameters
        ----------
            factor : real
                'factor' child.
        
        """

