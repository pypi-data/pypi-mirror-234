#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class repair_improve:
    fluent_name = ...
    child_names = ...
    allow_repair_at_boundaries = ...
    include_local_polyhedra_conversion_in_repair = ...
    command_names = ...

    def repair_poor_elements(self, ):
        """
        Report invalid and poor quality elements.
        """

    def improve_quality(self, ):
        """
        Tries to improve the mesh quality.
        """

    def repair(self, ):
        """
        Tries to repair mesh problems identified by mesh check.
        """

    def repair_face_handedness(self, repair: bool, disable_repair: bool):
        """
        Correct face handedness at left handed faces if possible.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
            disable_repair : bool
                'disable_repair' child.
        
        """

    def repair_face_node_order(self, ):
        """
        Reverse order of face nodes if needed.
        """

    def repair_wall_distance(self, repair: bool):
        """
        Correct wall distance at very high aspect ratio hexahedral/polyhedral cells.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
        
        """

