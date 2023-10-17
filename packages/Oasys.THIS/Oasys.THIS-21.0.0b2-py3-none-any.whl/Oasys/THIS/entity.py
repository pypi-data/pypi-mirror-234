import Oasys.gRPC


# Metaclass for static properties and constants
class EntityType(type):
    _consts = {'AIRBAG', 'AIRBAG_CHAMBER_DATA', 'AIRBAG_CPM_PART_DATA', 'AIRBAG_CPM_SENSORS', 'AIRBAG_CV_PART_DATA', 'AIRBAG_DATA', 'BEAM', 'BEAM_DISCRETE', 'BEAM_NORMAL', 'BEARING', 'BOUNDARY', 'BOUNDARY_DIS_NODAL_LOAD', 'BOUNDARY_DIS_RBODY_LOAD', 'BOUNDARY_PRES_NODAL_LOAD', 'BOUNDARY_VEL_NODAL_LOAD', 'BOUNDARY_VEL_RBODY_LOAD', 'CESE', 'CESE_DRAG_DATA', 'CESE_NODE_DATA', 'CESE_POINT_DATA', 'CESE_SEGMENT_DATA', 'CONTACT', 'CONTACT_ENERGIES', 'CONTACT_FORCES', 'CURVOUT', 'EM', 'EM_BOUNDARYOUT_DATA', 'EM_CIRCUIT0D_DATA', 'EM_CIRCUITRES_DATA', 'EM_CIRCUIT_DATA', 'EM_GLOBAL_DATA', 'EM_ISOPOTCONNOUT_DATA', 'EM_ISOPOTOUT_DATA', 'EM_NODE_DATA', 'EM_PARTDATA_DATA', 'EM_POINT_DATA', 'EM_RANDLESCELL_DATA', 'EM_RISC_DATA', 'EM_ROGOCOIL_DATA', 'FSI', 'FSI_SENSOR_DATA', 'FSI_SURFACE_DATA', 'GEOMETRIC_CONTACT', 'ICFD', 'ICFD_DRAG_DATA', 'ICFD_NODE_DATA', 'ICFD_POINT_DATA', 'ICFD_THERMAL_DATA', 'JOINT', 'JOINT_FLEXION_TORSION', 'JOINT_GENERALIZED', 'JOINT_JOINT', 'JOINT_TRANSLATIONAL', 'MASS', 'MODEL', 'NODAL_RB', 'NODAL_RB_BODY', 'NODAL_RB_PART', 'NODE', 'NODE_GROUP', 'NODE_GROUP_GROUPS', 'NODE_GROUP_NODES', 'PART', 'PART_GROUP', 'PBLAST', 'PBLAST_DATA', 'PBLAST_PART', 'PRETENSIONER', 'PRTUBE', 'PULLEY', 'RETRACTOR', 'RIGIDWALL', 'SEATBELT', 'SHELL', 'SLIPRING', 'SOLID', 'SPC', 'SPC_FORCES', 'SPC_MODEL', 'SPC_MOMENTS', 'SPC_SET', 'SPH', 'SPRING', 'SPRING_ROTATIONAL', 'SPRING_TRANSLATIONAL', 'SUBSYSTEM', 'THICK_SHELL', 'TRACER', 'WELD', 'WELD_ASSEMBLY', 'WELD_CONSTRAINED', 'WELD_GENERALISED', 'WELD_NON_NODAL', 'WELD_SOLID', 'WELD_SPOTWELD_BEAMS', 'X_SECTION'}

    def __getattr__(cls, name):
        if name in EntityType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Entity(Oasys.gRPC.OasysItem, metaclass=EntityType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
