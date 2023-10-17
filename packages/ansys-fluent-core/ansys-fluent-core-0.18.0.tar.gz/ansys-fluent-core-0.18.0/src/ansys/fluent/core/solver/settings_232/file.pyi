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
    convert_hanging_nodes_during_read = ...
    async_optimize = ...
    write_pdat = ...
    confirm_overwrite = ...
    auto_save = ...
    export = ...
    import_ = ...
    parametric_project = ...
    cffio_options = ...
    command_names = ...

    def define_macro(self, filename: str):
        """
        Save input to a named macro.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def execute_macro(self, macro_filename: str):
        """
        Run a previously defined macro.
        
        Parameters
        ----------
            macro_filename : str
                'macro_filename' child.
        
        """

    def read_macros(self, file_name: str):
        """
        Read macro definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
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

    def read_settings(self, file_name: str):
        """
        Read and set boundary conditions from specified file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_field_functions(self, file_name: str):
        """
        Read custom field-function definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_injections(self, file_name: str):
        """
        Read all DPM injections from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_profile(self, file_name: str):
        """
        Read boundary profile data (*.prof, *.csv). Default is *.prof.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_pdf(self, file_name: str):
        """
        Read a PDF file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_isat_table(self, file_name: str):
        """
        Read an ISAT table.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def show_configuration(self, ):
        """
        Display current release and version information.
        """

    def stop_macro(self, ):
        """
        Stop recording input to a macro.
        """

    def start_transcript(self, file_name: str):
        """
        Start recording input and output in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def stop_transcript(self, ):
        """
        Stop recording input and output and close the transcript file.
        """

    def data_file_options(self, reset_defined_derived_quantities: bool, derived_quantities: List[str]):
        """
        Set derived quantities to be written in data file.
        
        Parameters
        ----------
            reset_defined_derived_quantities : bool
                'reset_defined_derived_quantities' child.
            derived_quantities : typing.List[str]
                'derived_quantities' child.
        
        """

