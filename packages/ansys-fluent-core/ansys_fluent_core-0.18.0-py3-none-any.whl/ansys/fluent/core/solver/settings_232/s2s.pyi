#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class s2s:
    fluent_name = ...
    child_names = ...
    viewfactor_settings = ...
    clustering_settings = ...
    radiosity_solver_control = ...
    command_names = ...

    def compute_write_vf(self, file_name: str):
        """
        Compute/write surface clusters and view factors for S2S radiation model.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def compute_vf_accelerated(self, file_name: str):
        """
        Compute/Write view factors from existing surface clusters.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def compute_clusters_and_vf_accelerated(self, file_name: str):
        """
        Compute/Write surface cluster first and then view factors.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def compute_vf_only(self, file_name: str):
        """
        Compute/write view factors only.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_vf_file(self, file_name: str):
        """
        Read an S2S file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

