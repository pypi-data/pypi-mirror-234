#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class file:
    fluent_name = ...
    child_names = ...
    single_precision_coordinates = ...
    binary_legacy_files = ...
    cff_files = ...
    async_optimize = ...
    write_pdat = ...
    confirm_overwrite = ...
    export = ...
    import_ = ...
    parametric_project = ...
    command_names = ...

    def auto_save(self, ):
        """
        'auto_save' child.
        """

    def define_macro(self, filename: str):
        """
        Save input to a named macro.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def read(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_data' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case_setting(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_setting' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_data' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_mesh(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_mesh' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_journal(self, file_name_list: List[str]):
        """
        Read a journal file.
        
        Parameters
        ----------
            file_name_list : typing.List[str]
                'file_name_list' child.
        
        """

    def start_journal(self, file_name: str):
        """
        Start recording all input in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def stop_journal(self, ):
        """
        Stop recording input and close the journal file.
        """

    def replace_mesh(self, file_name: str):
        """
        'replace_mesh' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_type: str, file_name: str):
        """
        'write' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
        
        """

