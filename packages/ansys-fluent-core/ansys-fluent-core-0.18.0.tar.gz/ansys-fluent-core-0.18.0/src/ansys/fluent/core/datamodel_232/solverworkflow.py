#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
        self.FaceZone = self.__class__.FaceZone(service, rules, path + [("FaceZone", "")])
        self.Zone = self.__class__.Zone(service, rules, path + [("Zone", "")])
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.ZoneList = self.__class__.ZoneList(service, rules, path + [("ZoneList", "")])
        self.JournalCommand = self.__class__.JournalCommand(service, rules, "JournalCommand", path)
        self.TWF_AssociateMesh = self.__class__.TWF_AssociateMesh(service, rules, "TWF_AssociateMesh", path)
        self.TWF_BasicMachineDescription = self.__class__.TWF_BasicMachineDescription(service, rules, "TWF_BasicMachineDescription", path)
        self.TWF_BladeRowAnalysisScope = self.__class__.TWF_BladeRowAnalysisScope(service, rules, "TWF_BladeRowAnalysisScope", path)
        self.TWF_CompleteWorkflowSetup = self.__class__.TWF_CompleteWorkflowSetup(service, rules, "TWF_CompleteWorkflowSetup", path)
        self.TWF_CreateCFDModel = self.__class__.TWF_CreateCFDModel(service, rules, "TWF_CreateCFDModel", path)
        self.TWF_ImportMesh = self.__class__.TWF_ImportMesh(service, rules, "TWF_ImportMesh", path)
        self.TWF_MapRegionInfo = self.__class__.TWF_MapRegionInfo(service, rules, "TWF_MapRegionInfo", path)
        self.TWF_ReportDefMonitors = self.__class__.TWF_ReportDefMonitors(service, rules, "TWF_ReportDefMonitors", path)
        self.TWF_TurboPhysics = self.__class__.TWF_TurboPhysics(service, rules, "TWF_TurboPhysics", path)
        self.TWF_TurboRegionsZones = self.__class__.TWF_TurboRegionsZones(service, rules, "TWF_TurboRegionsZones", path)
        self.TWF_TurboSurfaces = self.__class__.TWF_TurboSurfaces(service, rules, "TWF_TurboSurfaces", path)
        self.TWF_TurboTopology = self.__class__.TWF_TurboTopology(service, rules, "TWF_TurboTopology", path)
        super().__init__(service, rules, path)

    class CellZone(PyNamedObjectContainer):
        """
        .
        """
        class _CellZone(PyMenu):
            """
            Singleton _CellZone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.ConnectedFaces = self.__class__.ConnectedFaces(service, rules, path + [("ConnectedFaces", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type List[str].
                """
                pass

            class ConnectedFaces(PyTextual):
                """
                Parameter ConnectedFaces of value type List[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _CellZone:
            return super().__getitem__(key)

    class FaceZone(PyNamedObjectContainer):
        """
        .
        """
        class _FaceZone(PyMenu):
            """
            Singleton _FaceZone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type List[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _FaceZone:
            return super().__getitem__(key)

    class Zone(PyNamedObjectContainer):
        """
        .
        """
        class _Zone(PyMenu):
            """
            Singleton _Zone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type List[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _Zone:
            return super().__getitem__(key)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.EnableTurboMeshing = self.__class__.EnableTurboMeshing(service, rules, path + [("EnableTurboMeshing", "")])
            super().__init__(service, rules, path)

        class EnableTurboMeshing(PyParameter):
            """
            Parameter EnableTurboMeshing of value type bool.
            """
            pass

    class ZoneList(PyMenu):
        """
        Singleton ZoneList.
        """
        def __init__(self, service, rules, path):
            self.CellZones = self.__class__.CellZones(service, rules, path + [("CellZones", "")])
            self.FaceZones = self.__class__.FaceZones(service, rules, path + [("FaceZones", "")])
            super().__init__(service, rules, path)

        class CellZones(PyTextual):
            """
            Parameter CellZones of value type List[str].
            """
            pass

        class FaceZones(PyTextual):
            """
            Parameter FaceZones of value type List[str].
            """
            pass

    class JournalCommand(PyCommand):
        """
        Command JournalCommand.

        Parameters
        ----------
        JournalString : str
        PythonJournal : bool

        Returns
        -------
        bool
        """
        pass

    class TWF_AssociateMesh(PyCommand):
        """
        Command TWF_AssociateMesh.

        Parameters
        ----------
        AMChildName : str
        AMSelectComponentScope : str
        UseWireframe : bool
        RenameCellZones : str
        DefaultAMRowNumList : List[str]
        DefaultAMCellZonesList : List[str]
        AMRowNumList : List[str]
        OldAMCellZonesList : List[str]
        NewAMCellZonesList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_BasicMachineDescription(PyCommand):
        """
        Command TWF_BasicMachineDescription.

        Parameters
        ----------
        ComponentType : str
        ComponentName : str
        NumRows : int
        RowNumList : List[str]
        OldRowNameList : List[str]
        NewRowNameList : List[str]
        OldRowTypeList : List[str]
        NewRowTypeList : List[str]
        OldNumOfBladesList : List[str]
        NewNumOfBladesList : List[str]
        OldEnableTipGapList : List[str]
        NewEnableTipGapList : List[str]
        CombustorType : str

        Returns
        -------
        bool
        """
        pass

    class TWF_BladeRowAnalysisScope(PyCommand):
        """
        Command TWF_BladeRowAnalysisScope.

        Parameters
        ----------
        ASChildName : str
        ASSelectComponent : str
        ASRowNumList : List[str]
        OldASIncludeRowList : List[str]
        NewASIncludeRowList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_CompleteWorkflowSetup(PyCommand):
        """
        Command TWF_CompleteWorkflowSetup.


        Returns
        -------
        bool
        """
        pass

    class TWF_CreateCFDModel(PyCommand):
        """
        Command TWF_CreateCFDModel.

        Parameters
        ----------
        CFDMChildName : str
        CFDMSelectMeshAssociation : str
        AxisOfRotation : str
        DelayCFDModelCreation : bool
        RestrictToFactors : bool
        EstimateNumBlades : bool
        CFDMRowNumList : List[str]
        OldCFDMNumOfBladesList : List[str]
        NewCFDMNumOfBladesList : List[str]
        OldCFDMModelBladesList : List[str]
        NewCFDMModelBladesList : List[str]
        OldCFDMAngleOffset : List[str]
        NewCFDMAngleOffset : List[str]
        OldCFDMBladesPerSectorList : List[str]
        NewCFDMBladesPerSectorList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_ImportMesh(PyCommand):
        """
        Command TWF_ImportMesh.

        Parameters
        ----------
        AddChild : str
        MeshFilePath : str
        MeshFilePath_old : str
        MeshName : str
        CellZoneNames : List[str]
        ListItemLevels : List[str]
        ListItemTitles : List[str]
        ListOfCellZones : str
        CellZones : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_MapRegionInfo(PyCommand):
        """
        Command TWF_MapRegionInfo.

        Parameters
        ----------
        MRChildName : str
        MRSelectCellZone : str
        UseWireframe : bool
        DefaultMRRegionNameList : List[str]
        DefaultMRFaceZoneList : List[str]
        MRRegionNameList : List[str]
        OldMRFaceZoneList : List[str]
        NewMRFaceZoneList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_ReportDefMonitors(PyCommand):
        """
        Command TWF_ReportDefMonitors.

        Parameters
        ----------
        RDIsoSurfaceNumList : List[str]
        OldCreateContourList : List[str]
        NewCreateContourList : List[str]
        TurboContoursList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboPhysics(PyCommand):
        """
        Command TWF_TurboPhysics.

        Parameters
        ----------
        States : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboRegionsZones(PyCommand):
        """
        Command TWF_TurboRegionsZones.

        Parameters
        ----------
        States : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboSurfaces(PyCommand):
        """
        Command TWF_TurboSurfaces.

        Parameters
        ----------
        NumIsoSurfaces : int
        IsoSurfaceNumList : List[str]
        OldIsoSurfaceNameList : List[str]
        NewIsoSurfaceNameList : List[str]
        OldIsoSurfaceValueList : List[str]
        NewIsoSurfaceValueList : List[str]
        SurfacesList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboTopology(PyCommand):
        """
        Command TWF_TurboTopology.

        Parameters
        ----------
        TopologyName : str
        UseWireframe : bool
        DefaultTopologyNameList : List[str]
        DefaultTopologyZoneList : List[str]
        TopologyNameList : List[str]
        OldTopologyZoneList : List[str]
        NewTopologyZoneList : List[str]

        Returns
        -------
        bool
        """
        pass

