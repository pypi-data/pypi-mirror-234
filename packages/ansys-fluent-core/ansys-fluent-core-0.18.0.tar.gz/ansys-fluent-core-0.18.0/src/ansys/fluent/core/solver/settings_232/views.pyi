#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class views:
    fluent_name = ...
    child_names = ...
    camera = ...
    display_states = ...
    command_names = ...

    def auto_scale(self, ):
        """
        'auto_scale' command.
        """

    def reset_to_default_view(self, ):
        """
        Reset view to front and center.
        """

    def delete_view(self, view_name: str):
        """
        Remove a view from the list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def last_view(self, ):
        """
        Return to the camera position before the last manipulation.
        """

    def next_view(self, ):
        """
        Return to the camera position after the current position in the stack.
        """

    def list_views(self, ):
        """
        List predefined and saved views.
        """

    def restore_view(self, view_name: str):
        """
        Use a saved view.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def read_views(self, filename: str):
        """
        Read views from a view file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def save_view(self, view_name: str):
        """
        Save the current view to the view list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def write_views(self, file_name: str, view_list: List[str]):
        """
        Write selected views to a view file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            view_list : typing.List[str]
                'view_list' child.
        
        """

