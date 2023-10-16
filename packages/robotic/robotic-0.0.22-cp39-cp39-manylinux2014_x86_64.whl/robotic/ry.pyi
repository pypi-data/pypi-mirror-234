"""rai bindings"""
from __future__ import annotations
import ry
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "ArgWord",
    "BotOp",
    "CameraView",
    "CameraViewSensor",
    "Ceres",
    "Config",
    "ConfigurationViewer",
    "ControlMode",
    "FS",
    "Feature",
    "Frame",
    "ImageViewer",
    "ImpType",
    "Ipopt",
    "JT",
    "KOMO",
    "KOMO_Objective",
    "LBFGS",
    "NLP",
    "NLP_Factory",
    "NLP_Solver",
    "NLP_SolverID",
    "NLP_SolverOptions",
    "NLopt",
    "OT",
    "OptBench_Skeleton_Handover",
    "OptBench_Skeleton_Pick",
    "OptBench_Skeleton_StackAndBalance",
    "OptBenchmark_InvKin_Endeff",
    "PathFinder",
    "PointCloudViewer",
    "ST",
    "SY",
    "Simulation",
    "SimulationEngine",
    "Skeleton",
    "SolverReturn",
    "XBall",
    "above",
    "aboveBox",
    "acceleration",
    "accumulatedCollisions",
    "adversarialDropper",
    "alignByInt",
    "angularVel",
    "augmentedLag",
    "bounce",
    "box",
    "boxGraspX",
    "boxGraspY",
    "boxGraspZ",
    "break",
    "bullet",
    "camera",
    "capsule",
    "closeGripper",
    "compiled",
    "contact",
    "contactComplementary",
    "contactConstraints",
    "contactStick",
    "cylinder",
    "dampMotion",
    "depthNoise",
    "distance",
    "downUp",
    "dynamic",
    "dynamicOn",
    "dynamicTrans",
    "end",
    "energy",
    "eq",
    "f",
    "forceBalance",
    "free",
    "gazeAt",
    "generic",
    "getStartGoalPath",
    "gradientDescent",
    "hingeX",
    "hingeY",
    "hingeZ",
    "identical",
    "ineq",
    "ineqB",
    "ineqP",
    "inside",
    "insideBox",
    "jointLimits",
    "jointState",
    "kinematic",
    "lift",
    "logBarrier",
    "magic",
    "magicTrans",
    "makeFree",
    "marker",
    "mesh",
    "moveGripper",
    "negDistance",
    "newton",
    "noPenetrations",
    "none",
    "objectImpulses",
    "oppose",
    "pairCollision_negScalar",
    "pairCollision_normal",
    "pairCollision_p1",
    "pairCollision_p2",
    "pairCollision_vector",
    "params_add",
    "params_clear",
    "params_file",
    "params_print",
    "phiTransXY",
    "physics",
    "physx",
    "pointCloud",
    "pose",
    "poseDiff",
    "poseEq",
    "poseRel",
    "position",
    "positionDiff",
    "positionEq",
    "positionRel",
    "push",
    "pushAndPlace",
    "qItself",
    "quad",
    "quasiStatic",
    "quasiStaticOn",
    "quatBall",
    "quaternion",
    "quaternionDiff",
    "quaternionRel",
    "raiPath",
    "relPosY",
    "restingOn",
    "rgbNoise",
    "rigid",
    "rprop",
    "scalarProductXX",
    "scalarProductXY",
    "scalarProductXZ",
    "scalarProductYX",
    "scalarProductYY",
    "scalarProductYZ",
    "scalarProductZZ",
    "sdf",
    "setRaiPath",
    "singleSquaredPenalty",
    "sos",
    "sphere",
    "spline",
    "squaredPenalty",
    "ssBox",
    "ssBoxElip",
    "ssCvx",
    "ssCylinder",
    "stable",
    "stableOn",
    "stableOnX",
    "stableOnY",
    "stablePose",
    "stableRelPose",
    "stableYPhi",
    "stableZero",
    "standingAbove",
    "tau",
    "test",
    "topBoxGrasp",
    "topBoxPlace",
    "touch",
    "touchBoxNormalX",
    "touchBoxNormalY",
    "touchBoxNormalZ",
    "trans3",
    "transAccelerations",
    "transVelocities",
    "transX",
    "transXY",
    "transXYPhi",
    "transY",
    "transYPhi",
    "transZ",
    "universal",
    "vectorX",
    "vectorXDiff",
    "vectorXRel",
    "vectorY",
    "vectorYDiff",
    "vectorYRel",
    "vectorZ",
    "vectorZDiff",
    "vectorZRel",
    "velocity"
]


class ArgWord():
    """
    Members:

      _left

      _right

      _sequence

      _path
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'_left': <ArgWord._left: 0>, '_right': <ArgWord._right: 1>, '_sequence': <ArgWord._sequence: 2>, '_path': <ArgWord._path: 3>}
    _left: ry.ArgWord # value = <ArgWord._left: 0>
    _path: ry.ArgWord # value = <ArgWord._path: 3>
    _right: ry.ArgWord # value = <ArgWord._right: 1>
    _sequence: ry.ArgWord # value = <ArgWord._sequence: 2>
    pass
class BotOp():
    """
    needs some docu!
    """
    def __init__(self, C: Config, useRealRobot: bool) -> None: ...
    def getCameraFxypxy(self, sensorName: str) -> arr: 
        """
        returns camera intrinsics
        """
    def getImageAndDepth(self, sensorName: str) -> tuple: 
        """
        returns image and depth from a camera sensor
        """
    def getImageDepthPcl(self, sensorName: str, globalCoordinates: bool = False) -> tuple: 
        """
        returns image, depth and point cloud (assuming sensor knows intrinsics) from a camera sensor, optionally in global instead of camera-frame-relative coordinates
        """
    def getKeyPressed(self) -> int: 
        """
        get key pressed in window at last sync
        """
    def getTimeToEnd(self) -> float: 
        """
        get time-to-go of the current spline reference that is tracked (use getTimeToEnd()<=0. to check if motion execution is done)
        """
    def get_q(self) -> arr: 
        """
        get the current (real) robot joint vector
        """
    def get_qDot(self) -> arr: 
        """
        get the current (real) robot joint velocities
        """
    def get_qHome(self) -> arr: 
        """
        returns home joint vector (defined as the configuration C when you created BotOp)
        """
    def get_t(self) -> float: 
        """
        returns the control time (absolute time managed by the high freq tracking controller)
        """
    def get_tauExternal(self) -> arr: 
        """
        get the current (real) robot joint torques (external: gravity & acceleration removed) -- each call averages from last call; first call might return nonsense!
        """
    def gripperClose(self, leftRight: ArgWord, force: float = 10.0, width: float = 0.05, speed: float = 0.1) -> None: 
        """
        close gripper
        """
    def gripperCloseGrasp(self, leftRight: ArgWord, objName: str, force: float = 10.0, width: float = 0.05, speed: float = 0.1) -> None: 
        """
        close gripper and indicate what should be grasped -- makes no different in real, but helps simulation to mimic grasping more reliably
        """
    def gripperDone(self, leftRight: ArgWord) -> bool: 
        """
        returns if gripper is done
        """
    def gripperMove(self, leftRight: ArgWord, width: float = 0.075, speed: float = 0.2) -> None: 
        """
        move the gripper to width (default: open)
        """
    def gripperPos(self, leftRight: ArgWord) -> float: 
        """
        returns the gripper pos
        """
    def hold(self, floating: bool = False, damping: bool = True) -> None: 
        """
        hold the robot with a trivial PD controller, floating means reference = real, without damping the robot is free floating
        """
    def home(self, C: Config) -> None: 
        """
        immediately drive the robot home (see get_qHome); keeps argument C synced; same as moveTo(qHome, 1., True); wait(C);
        """
    def move(self, path: arr, times: arr, overwrite: bool = False, overwriteCtrlTime: float = -1.0) -> None: 
        """
        core motion command: set a spline motion reference; if only a single time [T] is given for multiple waypoints, it assumes equal time spacing with TOTAL time T

        By default, the given spline is APPENDED to the current reference spline. The user can also enforce the given spline to overwrite the current reference starting at the given absolute ctrlTime. This allows implementation of reactive (e.g. MPC-style) control. However, the user needs to take care that overwriting is done in a smooth way, i.e., that the given spline starts with a pos/vel that is close to the pos/vel of the current reference at the given ctrlTime.
        """
    def moveAutoTimed(self, path: arr, maxVel: float = 1.0, maxAcc: float = 1.0) -> None: 
        """
        helper to execute a path (typically fine resolution, from KOMO or RRT) with equal time spacing chosen for given max vel/acc
        """
    def moveTo(self, q_target: arr, timeCost: float = 1.0, overwrite: bool = False) -> None: 
        """
        helper to move to a single joint vector target, where timing is chosen optimally based on the given timing cost

        When using overwrite, this immediately steers to the target -- use this as a well-timed reactive q_target controller
        """
    def setCompliance(self, J: arr, compliance: float = 0.5) -> None: 
        """
        set a task space compliant, where J defines the task space Jacobian, and compliance goes from 0 (no compliance) to 1 (full compliance, but still some damping)
        """
    def setControllerWriteData(self, arg0: int) -> None: 
        """
        [for internal debugging only] triggers writing control data into a file
        """
    def stop(self, C: Config) -> None: 
        """
        immediately stop the robot; keeps argument C synced; same as moveTo(get_q(), 1., True); wait(C);
        """
    def sync(self, C: Config, waitTime: float = 0.1) -> int: 
        """
        sync your workspace configuration C with the robot state
        """
    def wait(self, C: Config, forKeyPressed: bool = True, forTimeToEnd: bool = True) -> int: 
        """
        repeatedly sync your workspace C until a key is pressed or motion ends (optionally)
        """
    pass
class CameraView():
    def addSensor(self, name: str, frameAttached: str, width: int, height: int, focalLength: float = -1.0, orthoAbsHeight: float = -1.0, zRange: typing.List[float] = [], backgroundImageFile: str = '') -> None: ...
    def computeImageAndDepth(self, visualsOnly: bool = True) -> tuple: ...
    def computePointCloud(self, depth: numpy.ndarray, globalCoordinates: bool = True) -> numpy.ndarray[numpy.float64]: ...
    def computeSegmentation(self) -> numpy.ndarray[numpy.uint8]: ...
    def imageViewer(self) -> ImageViewer: ...
    def pointCloudViewer(self) -> PointCloudViewer: ...
    def segmentationViewer(self) -> ImageViewer: ...
    def selectSensor(self, name: str) -> None: ...
    def updateConfig(self, arg0: Config) -> None: ...
    pass
class CameraViewSensor():
    pass
class Config():
    """
    Core data structure to represent a kinematic configuration.
    """
    def __init__(self) -> None: 
        """
        initializes to an empty configuration, with no frames
        """
    def addConfigurationCopy(self, config: Config, tau: float = 1.0) -> None: ...
    def addFile(self, filename: str, namePrefix: str = '') -> Frame: 
        """
        add the contents of the file to C
        """
    def addFrame(self, name: str, parent: str = '', args: str = '') -> Frame: 
        """
        add a new frame to C; optionally make this a child to the given parent; use the Frame methods to set properties of the new frame
        """
    def animate(self) -> None: 
        """
        displays while articulating all dofs in a row
        """
    def attach(self, arg0: str, arg1: str) -> None: 
        """
        change the configuration by creating a rigid joint from frame1 to frame2, adopting their current relative pose. This also breaks the first joint that is parental to frame2 and reverses the topological order from frame2 to the broken joint
        """
    def clear(self) -> None: 
        """
        clear all frames and additional data; becomes the empty configuration, with no frames
        """
    def computeCollisions(self) -> None: 
        """
        call the broadphase collision engine (SWIFT++ or FCL) to generate the list of collisions (or near proximities) between all frame shapes that have the collision tag set non-zero
        """
    def copy(self, C2: Config) -> None: 
        """
        make C a (deep) copy of the given C2
        """
    def delFrame(self, frameName: str) -> None: 
        """
        destroy and remove a frame from C
        """
    def equationOfMotion(self, qdot: typing.List[float], gravity: bool) -> tuple: ...
    def eval(self, featureSymbol: FS, frames: StringA = [], scale: arr = array(1.e-05), target: arr = array(0.0078125), order: int = -1) -> tuple: 
        """
        evaluate a feature
        """
    def feature(self, featureSymbol: FS, frameNames: typing.List[str] = [], scale: typing.List[float] = [], target: typing.List[float] = [], order: int = -1) -> Feature: 
        """
        create a feature (a differentiable map from joint state to a vector space), as they're typically used for IK or optimization. See the dedicated tutorial for details. featureSymbol defines which mapping this is (position, vectors, collision distance, etc). many mapping refer to one or several frames, which need to be specified using frameNames
        """
    def frame(self, frameName: str) -> Frame: 
        """
        get access to a frame by name; use the Frame methods to set/get frame properties
        """
    def frames(self) -> typing.List[Frame]: ...
    def getCollisions(self, belowMargin: float = 1.0) -> list: 
        """
        return the results of collision computations: a list of 3 tuples with (frame1, frame2, distance). Optionally report only on distances below a margin To get really precise distances and penetrations use the FS.distance feature with the two frame names
        """
    def getDofIDs(self) -> typing.List[int]: ...
    def getFrame(self, frameName: str) -> Frame: 
        """
        get access to a frame by name; use the Frame methods to set/get frame properties
        """
    def getFrameDimension(self) -> int: 
        """
        get the total number of frames
        """
    def getFrameNames(self) -> typing.List[str]: 
        """
        get the list of frame names
        """
    @typing.overload
    def getFrameState(self) -> numpy.ndarray[numpy.float64]: 
        """
        get the frame state as a n-times-7 numpy matrix, with a 7D pose per frame

        TODO remove -> use individual frame!
        """
    @typing.overload
    def getFrameState(self, arg0: str) -> numpy.ndarray[numpy.float64]: ...
    def getJointDimension(self) -> int: 
        """
        get the total number of degrees of freedom
        """
    def getJointNames(self) -> StringA: 
        """
        get the list of joint names
        """
    def getJointState(self) -> arr: 
        """
        get the joint state as a numpy vector, optionally only for a subset of joints specified as list of joint names
        """
    def getTotalPenetration(self) -> float: 
        """
        returns the sum of all penetrations
        """
    def makeObjectsConvex(self) -> None: 
        """
        remake all meshes associated with all frames to become their convex hull
        """
    def report(self) -> str: ...
    def selectJoints(self, jointNames: typing.List[str], notThose: bool = False) -> None: 
        """
        redefine what are considered the DOFs of this configuration: only joints listed in jointNames are considered part of the joint state and define the number of DOFs
        """
    @typing.overload
    def setFrameState(self, X: typing.List[float], frames: typing.List[str] = []) -> None: 
        """
        set the frame state, optionally only for a subset of frames specified as list of frame names

        set the frame state, optionally only for a subset of frames specified as list of frame names
        """
    @typing.overload
    def setFrameState(self, X: numpy.ndarray, frames: typing.List[str] = []) -> None: ...
    def setJointState(self, q: arr, joints: list = []) -> None: 
        """
        set the joint state, optionally only for a subset of joints specified as list of joint names
        """
    def setJointStateSlice(self, arg0: typing.List[float], arg1: int) -> None: ...
    def sortFrames(self) -> None: 
        """
        resort the internal order of frames according to the tree topology. This is important before saving the configuration.
        """
    def stepDynamics(self, qdot: typing.List[float], u_control: typing.List[float], tau: float, dynamicNoise: float, gravity: bool) -> numpy.ndarray[numpy.float64]: ...
    def view(self, pause: bool = False, message: str = None) -> int: 
        """
        open a view window for the configuration
        """
    def view_close(self) -> None: 
        """
        close the view
        """
    def view_getScreenshot(self) -> numpy.ndarray[numpy.uint8]: ...
    def view_playVideo(self, delay: float = 1.0, saveVideoPath: str = None) -> None: ...
    def view_recopyMeshes(self) -> None: ...
    def watchFile(self, arg0: str) -> None: 
        """
        launch a viewer that listents (inode) to changes of a file (made by you in an editor), and reloads, displays and animates the configuration whenever the file is changed
        """
    def write(self) -> str: 
        """
        write the full configuration in a string (roughly yaml), e.g. for file export
        """
    def writeCollada(self, arg0: str, arg1: str) -> None: 
        """
        write the full configuration in a collada file for export
        """
    def writeURDF(self) -> str: 
        """
        write the full configuration as URDF in a string, e.g. for file export
        """
    pass
class ConfigurationViewer():
    pass
class ControlMode():
    """
    Members:

      none

      position

      velocity

      acceleration

      spline
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'none': <ControlMode.none: 0>, 'position': <ControlMode.position: 1>, 'velocity': <ControlMode.velocity: 2>, 'acceleration': <ControlMode.acceleration: 3>, 'spline': <ControlMode.spline: 5>}
    acceleration: ry.ControlMode # value = <ControlMode.acceleration: 3>
    none: ry.ControlMode # value = <ControlMode.none: 0>
    position: ry.ControlMode # value = <ControlMode.position: 1>
    spline: ry.ControlMode # value = <ControlMode.spline: 5>
    velocity: ry.ControlMode # value = <ControlMode.velocity: 2>
    pass
class FS():
    """
    Members:

      position

      positionDiff

      positionRel

      quaternion

      quaternionDiff

      quaternionRel

      pose

      poseDiff

      poseRel

      vectorX

      vectorXDiff

      vectorXRel

      vectorY

      vectorYDiff

      vectorYRel

      vectorZ

      vectorZDiff

      vectorZRel

      scalarProductXX

      scalarProductXY

      scalarProductXZ

      scalarProductYX

      scalarProductYY

      scalarProductYZ

      scalarProductZZ

      gazeAt

      angularVel

      accumulatedCollisions

      jointLimits

      distance

      negDistance

      oppose

      qItself

      jointState

      aboveBox

      insideBox

      pairCollision_negScalar

      pairCollision_vector

      pairCollision_normal

      pairCollision_p1

      pairCollision_p2

      standingAbove

      physics

      contactConstraints

      energy

      transAccelerations

      transVelocities
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'position': <FS.position: 0>, 'positionDiff': <FS.positionDiff: 1>, 'positionRel': <FS.positionRel: 2>, 'quaternion': <FS.quaternion: 3>, 'quaternionDiff': <FS.quaternionDiff: 4>, 'quaternionRel': <FS.quaternionRel: 5>, 'pose': <FS.pose: 6>, 'poseDiff': <FS.poseDiff: 7>, 'poseRel': <FS.poseRel: 8>, 'vectorX': <FS.vectorX: 9>, 'vectorXDiff': <FS.vectorXDiff: 10>, 'vectorXRel': <FS.vectorXRel: 11>, 'vectorY': <FS.vectorY: 12>, 'vectorYDiff': <FS.vectorYDiff: 13>, 'vectorYRel': <FS.vectorYRel: 14>, 'vectorZ': <FS.vectorZ: 15>, 'vectorZDiff': <FS.vectorZDiff: 16>, 'vectorZRel': <FS.vectorZRel: 17>, 'scalarProductXX': <FS.scalarProductXX: 18>, 'scalarProductXY': <FS.scalarProductXY: 19>, 'scalarProductXZ': <FS.scalarProductXZ: 20>, 'scalarProductYX': <FS.scalarProductYX: 21>, 'scalarProductYY': <FS.scalarProductYY: 22>, 'scalarProductYZ': <FS.scalarProductYZ: 23>, 'scalarProductZZ': <FS.scalarProductZZ: 24>, 'gazeAt': <FS.gazeAt: 25>, 'angularVel': <FS.angularVel: 26>, 'accumulatedCollisions': <FS.accumulatedCollisions: 27>, 'jointLimits': <FS.jointLimits: 28>, 'distance': <FS.distance: 29>, 'negDistance': <FS.distance: 29>, 'oppose': <FS.oppose: 30>, 'qItself': <FS.qItself: 31>, 'jointState': <FS.qItself: 31>, 'aboveBox': <FS.aboveBox: 33>, 'insideBox': <FS.insideBox: 34>, 'pairCollision_negScalar': <FS.pairCollision_negScalar: 35>, 'pairCollision_vector': <FS.pairCollision_vector: 36>, 'pairCollision_normal': <FS.pairCollision_normal: 37>, 'pairCollision_p1': <FS.pairCollision_p1: 38>, 'pairCollision_p2': <FS.pairCollision_p2: 39>, 'standingAbove': <FS.standingAbove: 40>, 'physics': <FS.physics: 41>, 'contactConstraints': <FS.contactConstraints: 42>, 'energy': <FS.energy: 43>, 'transAccelerations': <FS.transAccelerations: 44>, 'transVelocities': <FS.transVelocities: 45>}
    aboveBox: ry.FS # value = <FS.aboveBox: 33>
    accumulatedCollisions: ry.FS # value = <FS.accumulatedCollisions: 27>
    angularVel: ry.FS # value = <FS.angularVel: 26>
    contactConstraints: ry.FS # value = <FS.contactConstraints: 42>
    distance: ry.FS # value = <FS.distance: 29>
    energy: ry.FS # value = <FS.energy: 43>
    gazeAt: ry.FS # value = <FS.gazeAt: 25>
    insideBox: ry.FS # value = <FS.insideBox: 34>
    jointLimits: ry.FS # value = <FS.jointLimits: 28>
    jointState: ry.FS # value = <FS.qItself: 31>
    negDistance: ry.FS # value = <FS.distance: 29>
    oppose: ry.FS # value = <FS.oppose: 30>
    pairCollision_negScalar: ry.FS # value = <FS.pairCollision_negScalar: 35>
    pairCollision_normal: ry.FS # value = <FS.pairCollision_normal: 37>
    pairCollision_p1: ry.FS # value = <FS.pairCollision_p1: 38>
    pairCollision_p2: ry.FS # value = <FS.pairCollision_p2: 39>
    pairCollision_vector: ry.FS # value = <FS.pairCollision_vector: 36>
    physics: ry.FS # value = <FS.physics: 41>
    pose: ry.FS # value = <FS.pose: 6>
    poseDiff: ry.FS # value = <FS.poseDiff: 7>
    poseRel: ry.FS # value = <FS.poseRel: 8>
    position: ry.FS # value = <FS.position: 0>
    positionDiff: ry.FS # value = <FS.positionDiff: 1>
    positionRel: ry.FS # value = <FS.positionRel: 2>
    qItself: ry.FS # value = <FS.qItself: 31>
    quaternion: ry.FS # value = <FS.quaternion: 3>
    quaternionDiff: ry.FS # value = <FS.quaternionDiff: 4>
    quaternionRel: ry.FS # value = <FS.quaternionRel: 5>
    scalarProductXX: ry.FS # value = <FS.scalarProductXX: 18>
    scalarProductXY: ry.FS # value = <FS.scalarProductXY: 19>
    scalarProductXZ: ry.FS # value = <FS.scalarProductXZ: 20>
    scalarProductYX: ry.FS # value = <FS.scalarProductYX: 21>
    scalarProductYY: ry.FS # value = <FS.scalarProductYY: 22>
    scalarProductYZ: ry.FS # value = <FS.scalarProductYZ: 23>
    scalarProductZZ: ry.FS # value = <FS.scalarProductZZ: 24>
    standingAbove: ry.FS # value = <FS.standingAbove: 40>
    transAccelerations: ry.FS # value = <FS.transAccelerations: 44>
    transVelocities: ry.FS # value = <FS.transVelocities: 45>
    vectorX: ry.FS # value = <FS.vectorX: 9>
    vectorXDiff: ry.FS # value = <FS.vectorXDiff: 10>
    vectorXRel: ry.FS # value = <FS.vectorXRel: 11>
    vectorY: ry.FS # value = <FS.vectorY: 12>
    vectorYDiff: ry.FS # value = <FS.vectorYDiff: 13>
    vectorYRel: ry.FS # value = <FS.vectorYRel: 14>
    vectorZ: ry.FS # value = <FS.vectorZ: 15>
    vectorZDiff: ry.FS # value = <FS.vectorZDiff: 16>
    vectorZRel: ry.FS # value = <FS.vectorZRel: 17>
    pass
class Feature():
    """
    todo doc
    """
    def description(self, arg0: Config) -> str: ...
    def eval(self, arg0: Config) -> tuple: ...
    def setOrder(self, arg0: int) -> Feature: ...
    def setScale(self, arg0: arr) -> Feature: ...
    def setTarget(self, arg0: arr) -> Feature: ...
    pass
class Frame():
    """
    todo doc
    """
    def addAttribute(self, arg0: str, arg1: float) -> Frame: ...
    def addAttributes(self, arg0: dict) -> None: 
        """
        add/set attributes for the frame
        """
    def getAttributes(self) -> dict: 
        """
        get frame attributes
        """
    def getJointState(self) -> arr: ...
    def getMeshPoints(self) -> arr: ...
    def getMeshTriangles(self) -> uintA: ...
    def getPosition(self) -> arr: ...
    def getQuaternion(self) -> arr: ...
    def getRelativePosition(self) -> arr: ...
    def getRelativeQuaternion(self) -> arr: ...
    def getRotationMatrix(self) -> arr: ...
    def getSize(self) -> arr: ...
    def info(self) -> dict: ...
    def setColor(self, arg0: arr) -> Frame: ...
    def setContact(self, arg0: int) -> Frame: ...
    def setJoint(self, arg0: JT) -> Frame: ...
    def setJointState(self, arg0: arr) -> Frame: ...
    def setMass(self, arg0: float) -> Frame: ...
    def setMeshAsLines(self, arg0: typing.List[float]) -> None: ...
    def setParent(self, parent: Frame, keepAbsolutePose_and_adaptRelativePose: bool = False, checkForLoop: bool = False) -> Frame: ...
    def setPointCloud(self, points: numpy.ndarray, colors: numpy.ndarray[numpy.uint8] = array([], dtype=uint8)) -> None: ...
    def setPose(self, arg0: str) -> None: ...
    def setPosition(self, arg0: arr) -> Frame: ...
    def setQuaternion(self, arg0: arr) -> Frame: ...
    def setRelativePose(self, arg0: str) -> None: ...
    def setRelativePosition(self, arg0: arr) -> Frame: ...
    def setRelativeQuaternion(self, arg0: arr) -> Frame: ...
    def setShape(self, type: ST, size: arr) -> Frame: ...
    def unLink(self) -> Frame: ...
    @property
    def name(self) -> rai::String:
        """
        :type: rai::String
        """
    @name.setter
    def name(self, arg0: rai::String) -> None:
        pass
    pass
class ImageViewer():
    pass
class ImpType():
    """
    Members:

      closeGripper

      moveGripper

      depthNoise

      rgbNoise

      adversarialDropper

      objectImpulses

      noPenetrations
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'closeGripper': <ImpType.closeGripper: 0>, 'moveGripper': <ImpType.moveGripper: 1>, 'depthNoise': <ImpType.depthNoise: 2>, 'rgbNoise': <ImpType.rgbNoise: 3>, 'adversarialDropper': <ImpType.adversarialDropper: 4>, 'objectImpulses': <ImpType.objectImpulses: 5>, 'noPenetrations': <ImpType.noPenetrations: 7>}
    adversarialDropper: ry.ImpType # value = <ImpType.adversarialDropper: 4>
    closeGripper: ry.ImpType # value = <ImpType.closeGripper: 0>
    depthNoise: ry.ImpType # value = <ImpType.depthNoise: 2>
    moveGripper: ry.ImpType # value = <ImpType.moveGripper: 1>
    noPenetrations: ry.ImpType # value = <ImpType.noPenetrations: 7>
    objectImpulses: ry.ImpType # value = <ImpType.objectImpulses: 5>
    rgbNoise: ry.ImpType # value = <ImpType.rgbNoise: 3>
    pass
class JT():
    """
    Members:

      hingeX

      hingeY

      hingeZ

      transX

      transY

      transZ

      transXY

      trans3

      transXYPhi

      transYPhi

      universal

      rigid

      quatBall

      phiTransXY

      XBall

      free

      generic

      tau
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    XBall: ry.JT # value = <JT.XBall: 15>
    __members__: dict # value = {'hingeX': <JT.hingeX: 1>, 'hingeY': <JT.hingeY: 2>, 'hingeZ': <JT.hingeZ: 3>, 'transX': <JT.transX: 4>, 'transY': <JT.transY: 5>, 'transZ': <JT.transZ: 6>, 'transXY': <JT.transXY: 7>, 'trans3': <JT.trans3: 8>, 'transXYPhi': <JT.transXYPhi: 9>, 'transYPhi': <JT.transYPhi: 10>, 'universal': <JT.universal: 11>, 'rigid': <JT.rigid: 12>, 'quatBall': <JT.quatBall: 13>, 'phiTransXY': <JT.phiTransXY: 14>, 'XBall': <JT.XBall: 15>, 'free': <JT.free: 16>, 'generic': <JT.generic: 17>, 'tau': <JT.tau: 18>}
    free: ry.JT # value = <JT.free: 16>
    generic: ry.JT # value = <JT.generic: 17>
    hingeX: ry.JT # value = <JT.hingeX: 1>
    hingeY: ry.JT # value = <JT.hingeY: 2>
    hingeZ: ry.JT # value = <JT.hingeZ: 3>
    phiTransXY: ry.JT # value = <JT.phiTransXY: 14>
    quatBall: ry.JT # value = <JT.quatBall: 13>
    rigid: ry.JT # value = <JT.rigid: 12>
    tau: ry.JT # value = <JT.tau: 18>
    trans3: ry.JT # value = <JT.trans3: 8>
    transX: ry.JT # value = <JT.transX: 4>
    transXY: ry.JT # value = <JT.transXY: 7>
    transXYPhi: ry.JT # value = <JT.transXYPhi: 9>
    transY: ry.JT # value = <JT.transY: 5>
    transYPhi: ry.JT # value = <JT.transYPhi: 10>
    transZ: ry.JT # value = <JT.transZ: 6>
    universal: ry.JT # value = <JT.universal: 11>
    pass
class KOMO():
    """
    Constrained solver to optimize configurations or paths. (KOMO = k-order Markov Optimization)
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, config: Config, phases: float, slicesPerPhase: int, kOrder: int, enableCollisions: bool) -> None: ...
    def addControlObjective(self, times: arr, order: int, scale: float = 1.0, target: arr = array(0.0078125), deltaFromSlice: int = 0, deltaToSlice: int = 0) -> Objective: ...
    @staticmethod
    def addInteraction_elasticBounce(*args, **kwargs) -> typing.Any: ...
    def addModeSwitch(self, times: arr, newMode: SY, frames: StringA, firstSwitch: bool = True) -> None: ...
    @staticmethod
    def addObjective(*args, **kwargs) -> typing.Any: ...
    def addQuaternionNorms(self, times: arr = array(0.0078125), scale: float = 3.0, hard: bool = True) -> None: ...
    def addTimeOptimization(self) -> None: ...
    def clearObjectives(self) -> None: ...
    def getFeatureNames(self) -> StringA: 
        """
        returns a long list of features (per time slice!), to be used by an NLP_Solver
        """
    def getForceInteractions(self) -> list: ...
    def getFrameState(self, arg0: int) -> arr: ...
    def getPath(self) -> arr: ...
    def getPathFrames(self) -> arr: ...
    def getPathTau(self) -> arr: ...
    def getPath_qAll(self) -> arrA: ...
    def getReport(self, arg0: bool) -> dict: ...
    def getT(self) -> int: ...
    def initOrg(self) -> None: ...
    def initPhaseWithDofsPath(self, t_phase: int, dofIDs: uintA, path: arr, autoResamplePath: bool = False) -> None: ...
    def initRandom(self, verbose: int = 0) -> None: ...
    def initWithConstant(self, q: arr) -> None: ...
    def initWithPath_qOrg(self, q: arr) -> None: ...
    def initWithWaypoints(self, waypoints: arrA, waypointSlicesPerPhase: int = 1, interpolate: bool = False, verbose: int = -1) -> uintA: ...
    def nlp(self) -> NLP: 
        """
        return the problem NLP
        """
    def report(self, plotOverTime: bool = False) -> dict: 
        """
        returns a dict with full report on features, optionally plotting costs/violations over time
        """
    def reportProblem(self) -> str: ...
    def setConfig(self, config: Config, enableCollisions: bool) -> None: ...
    def setTiming(self, phases: float, slicesPerPhase: int, durationPerPhase: float, kOrder: int) -> None: ...
    def updateRootObjects(self, config: Config) -> None: 
        """
        update root frames (without parents) within all KOMO configurations
        """
    def view(self, pause: bool = False, txt: str = None) -> int: ...
    def view_close(self) -> None: ...
    def view_play(self, pause: bool = False, delay: float = 0.1, saveVideoPath: str = None) -> int: ...
    pass
class KOMO_Objective():
    pass
class NLP():
    """
    Representation of a Nonlinear Mathematical Program
    """
    def evaluate(self, arg0: arr) -> typing.Tuple[arr, arr]: 
        """
        query the NLP at a point $x$; returns the tuple $(phi,J)$, which is the feature vector and its Jacobian; features define cost terms, sum-of-square (sos) terms, inequalities, and equalities depending on 'getFeatureTypes'
        """
    def getBounds(self) -> typing.Tuple[arr, arr]: 
        """
        returns the tuple $(b_{lo},b_{up})$, where both vectors are of same dimensionality of $x$ (or size zero, if there are no bounds)
        """
    def getDimension(self) -> int: 
        """
        return the dimensionality of $x$
        """
    def getFHessian(self, arg0: arr) -> arr: 
        """
        returns Hessian of the sum of $f$-terms
        """
    def getFeatureTypes(self) -> typing.List[ObjectiveType]: ...
    def getInitializationSample(self, previousOptima: arr = array(0.0078125)) -> arr: 
        """
        returns a sample (e.g. uniform within bounds) to initialize an optimization -- not necessarily feasible
        """
    def report(self, arg0: int) -> str: 
        """
        displays semantic information on the last query
        """
    pass
class NLP_Factory(NLP):
    def __init__(self) -> None: ...
    def setBounds(self, arg0: arr, arg1: arr) -> None: ...
    def setDimension(self, arg0: int) -> None: ...
    def setEvalCallback(self, arg0: typing.Callable[[arr], typing.Tuple[arr, arr]]) -> None: ...
    @staticmethod
    def setFeatureTypes(*args, **kwargs) -> typing.Any: ...
    def testCallingEvalCallback(self, arg0: arr) -> typing.Tuple[arr, arr]: ...
    pass
class NLP_Solver():
    """
    An interface to portfolio of solvers
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, problem: NLP, verbose: int = 0) -> None: ...
    def getOptions(self) -> NLP_SolverOptions: ...
    def getTrace_J(self) -> arr: ...
    def getTrace_costs(self) -> arr: ...
    def getTrace_phi(self) -> arr: ...
    def getTrace_x(self) -> arr: ...
    def reportLagrangeGradients(self, arg0: StringA) -> dict: ...
    def setOptions(self, verbose: int = 1, stopTolerance: float = 0.01, stopFTolerance: float = -1.0, stopGTolerance: float = -1.0, stopEvals: int = 1000, maxStep: float = 0.2, damping: float = 1.0, stepInc: float = 1.5, stepDec: float = 0.5, wolfe: float = 0.01, muInit: float = 1.0, muInc: float = 5.0, muMax: float = 10000.0, muLBInit: float = 0.1, muLBDec: float = 0.2) -> NLP_Solver: 
        """
        set solver options
        """
    def setProblem(self, arg0: NLP) -> NLP_Solver: ...
    def setSolver(self, arg0: NLP_SolverID) -> NLP_Solver: ...
    def setTracing(self, arg0: bool, arg1: bool, arg2: bool, arg3: bool) -> NLP_Solver: ...
    def solve(self, resampleInitialization: int = -1) -> SolverReturn: ...
    pass
class NLP_SolverID():
    """
    Members:

      gradientDescent

      rprop

      LBFGS

      newton

      augmentedLag

      squaredPenalty

      logBarrier

      singleSquaredPenalty

      NLopt

      Ipopt

      Ceres
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Ceres: ry.NLP_SolverID # value = <NLP_SolverID.Ceres: 10>
    Ipopt: ry.NLP_SolverID # value = <NLP_SolverID.Ipopt: 9>
    LBFGS: ry.NLP_SolverID # value = <NLP_SolverID.LBFGS: 2>
    NLopt: ry.NLP_SolverID # value = <NLP_SolverID.NLopt: 8>
    __members__: dict # value = {'gradientDescent': <NLP_SolverID.gradientDescent: 0>, 'rprop': <NLP_SolverID.rprop: 1>, 'LBFGS': <NLP_SolverID.LBFGS: 2>, 'newton': <NLP_SolverID.newton: 3>, 'augmentedLag': <NLP_SolverID.augmentedLag: 4>, 'squaredPenalty': <NLP_SolverID.squaredPenalty: 5>, 'logBarrier': <NLP_SolverID.logBarrier: 6>, 'singleSquaredPenalty': <NLP_SolverID.singleSquaredPenalty: 7>, 'NLopt': <NLP_SolverID.NLopt: 8>, 'Ipopt': <NLP_SolverID.Ipopt: 9>, 'Ceres': <NLP_SolverID.Ceres: 10>}
    augmentedLag: ry.NLP_SolverID # value = <NLP_SolverID.augmentedLag: 4>
    gradientDescent: ry.NLP_SolverID # value = <NLP_SolverID.gradientDescent: 0>
    logBarrier: ry.NLP_SolverID # value = <NLP_SolverID.logBarrier: 6>
    newton: ry.NLP_SolverID # value = <NLP_SolverID.newton: 3>
    rprop: ry.NLP_SolverID # value = <NLP_SolverID.rprop: 1>
    singleSquaredPenalty: ry.NLP_SolverID # value = <NLP_SolverID.singleSquaredPenalty: 7>
    squaredPenalty: ry.NLP_SolverID # value = <NLP_SolverID.squaredPenalty: 5>
    pass
class NLP_SolverOptions():
    """
    solver options
    """
    def __init__(self) -> None: ...
    def dict(self) -> dict: ...
    def set_damping(self, arg0: float) -> NLP_SolverOptions: ...
    def set_maxStep(self, arg0: float) -> NLP_SolverOptions: ...
    def set_muInc(self, arg0: float) -> NLP_SolverOptions: ...
    def set_muInit(self, arg0: float) -> NLP_SolverOptions: ...
    def set_muLBDec(self, arg0: float) -> NLP_SolverOptions: ...
    def set_muLBInit(self, arg0: float) -> NLP_SolverOptions: ...
    def set_muMax(self, arg0: float) -> NLP_SolverOptions: ...
    def set_stepDec(self, arg0: float) -> NLP_SolverOptions: ...
    def set_stepInc(self, arg0: float) -> NLP_SolverOptions: ...
    def set_stopEvals(self, arg0: int) -> NLP_SolverOptions: ...
    def set_stopFTolerance(self, arg0: float) -> NLP_SolverOptions: ...
    def set_stopGTolerance(self, arg0: float) -> NLP_SolverOptions: ...
    def set_stopTolerance(self, arg0: float) -> NLP_SolverOptions: ...
    def set_verbose(self, arg0: int) -> NLP_SolverOptions: ...
    def set_wolfe(self, arg0: float) -> NLP_SolverOptions: ...
    pass
class OT():
    """
    Members:

      none

      f

      sos

      ineq

      eq

      ineqB

      ineqP
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'none': <OT.none: 0>, 'f': <OT.f: 1>, 'sos': <OT.sos: 2>, 'ineq': <OT.ineq: 3>, 'eq': <OT.eq: 4>, 'ineqB': <OT.ineqB: 5>, 'ineqP': <OT.ineqP: 6>}
    eq: ry.OT # value = <OT.eq: 4>
    f: ry.OT # value = <OT.f: 1>
    ineq: ry.OT # value = <OT.ineq: 3>
    ineqB: ry.OT # value = <OT.ineqB: 5>
    ineqP: ry.OT # value = <OT.ineqP: 6>
    none: ry.OT # value = <OT.none: 0>
    sos: ry.OT # value = <OT.sos: 2>
    pass
class OptBench_Skeleton_Handover():
    def __init__(self, arg0: ArgWord) -> None: ...
    def get(self) -> NLP: ...
    pass
class OptBench_Skeleton_Pick():
    def __init__(self, arg0: ArgWord) -> None: ...
    def get(self) -> NLP: ...
    pass
class OptBench_Skeleton_StackAndBalance():
    def __init__(self, arg0: ArgWord) -> None: ...
    def get(self) -> NLP: ...
    pass
class OptBenchmark_InvKin_Endeff():
    def __init__(self, arg0: str, arg1: bool) -> None: ...
    def get(self) -> NLP: ...
    pass
class PathFinder():
    """
    todo doc
    """
    def __init__(self) -> None: ...
    def setExplicitCollisionPairs(self, collisionPairs: StringA) -> PathFinder: ...
    def setProblem(self, Configuration: Config, starts: arr, goals: arr) -> PathFinder: ...
    def solve(self) -> SolverReturn: ...
    def step(self) -> bool: ...
    pass
class PointCloudViewer():
    pass
class ST():
    """
    Members:

      none

      box

      sphere

      capsule

      mesh

      cylinder

      marker

      pointCloud

      ssCvx

      ssBox

      ssCylinder

      ssBoxElip

      quad

      camera

      sdf
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'none': <ST.none: -1>, 'box': <ST.box: 0>, 'sphere': <ST.sphere: 1>, 'capsule': <ST.capsule: 2>, 'mesh': <ST.mesh: 3>, 'cylinder': <ST.cylinder: 4>, 'marker': <ST.marker: 5>, 'pointCloud': <ST.pointCloud: 6>, 'ssCvx': <ST.ssCvx: 7>, 'ssBox': <ST.ssBox: 8>, 'ssCylinder': <ST.ssCylinder: 9>, 'ssBoxElip': <ST.ssBoxElip: 10>, 'quad': <ST.quad: 11>, 'camera': <ST.camera: 12>, 'sdf': <ST.sdf: 13>}
    box: ry.ST # value = <ST.box: 0>
    camera: ry.ST # value = <ST.camera: 12>
    capsule: ry.ST # value = <ST.capsule: 2>
    cylinder: ry.ST # value = <ST.cylinder: 4>
    marker: ry.ST # value = <ST.marker: 5>
    mesh: ry.ST # value = <ST.mesh: 3>
    none: ry.ST # value = <ST.none: -1>
    pointCloud: ry.ST # value = <ST.pointCloud: 6>
    quad: ry.ST # value = <ST.quad: 11>
    sdf: ry.ST # value = <ST.sdf: 13>
    sphere: ry.ST # value = <ST.sphere: 1>
    ssBox: ry.ST # value = <ST.ssBox: 8>
    ssBoxElip: ry.ST # value = <ST.ssBoxElip: 10>
    ssCvx: ry.ST # value = <ST.ssCvx: 7>
    ssCylinder: ry.ST # value = <ST.ssCylinder: 9>
    pass
class SY():
    """
    Members:

      touch

      above

      inside

      oppose

      restingOn

      poseEq

      positionEq

      stableRelPose

      stablePose

      stable

      stableOn

      dynamic

      dynamicOn

      dynamicTrans

      quasiStatic

      quasiStaticOn

      downUp

      break

      stableZero

      contact

      contactStick

      contactComplementary

      bounce

      push

      magic

      magicTrans

      pushAndPlace

      topBoxGrasp

      topBoxPlace

      dampMotion

      identical

      alignByInt

      makeFree

      forceBalance

      relPosY

      touchBoxNormalX

      touchBoxNormalY

      touchBoxNormalZ

      boxGraspX

      boxGraspY

      boxGraspZ

      lift

      stableYPhi

      stableOnX

      stableOnY

      end
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'touch': <SY.touch: 0>, 'above': <SY.above: 1>, 'inside': <SY.inside: 2>, 'oppose': <SY.oppose: 3>, 'restingOn': <SY.restingOn: 4>, 'poseEq': <SY.poseEq: 5>, 'positionEq': <SY.positionEq: 6>, 'stableRelPose': <SY.stableRelPose: 7>, 'stablePose': <SY.stablePose: 8>, 'stable': <SY.stable: 9>, 'stableOn': <SY.stableOn: 10>, 'dynamic': <SY.dynamic: 11>, 'dynamicOn': <SY.dynamicOn: 12>, 'dynamicTrans': <SY.dynamicTrans: 13>, 'quasiStatic': <SY.quasiStatic: 14>, 'quasiStaticOn': <SY.quasiStaticOn: 15>, 'downUp': <SY.downUp: 16>, 'break': <SY.break: 17>, 'stableZero': <SY.stableZero: 18>, 'contact': <SY.contact: 19>, 'contactStick': <SY.contactStick: 20>, 'contactComplementary': <SY.contactComplementary: 21>, 'bounce': <SY.bounce: 22>, 'push': <SY.push: 23>, 'magic': <SY.magic: 24>, 'magicTrans': <SY.magicTrans: 25>, 'pushAndPlace': <SY.pushAndPlace: 26>, 'topBoxGrasp': <SY.topBoxGrasp: 27>, 'topBoxPlace': <SY.topBoxPlace: 28>, 'dampMotion': <SY.dampMotion: 29>, 'identical': <SY.identical: 30>, 'alignByInt': <SY.alignByInt: 31>, 'makeFree': <SY.makeFree: 32>, 'forceBalance': <SY.forceBalance: 33>, 'relPosY': <SY.relPosY: 34>, 'touchBoxNormalX': <SY.touchBoxNormalX: 35>, 'touchBoxNormalY': <SY.touchBoxNormalY: 36>, 'touchBoxNormalZ': <SY.touchBoxNormalZ: 37>, 'boxGraspX': <SY.boxGraspX: 38>, 'boxGraspY': <SY.boxGraspY: 39>, 'boxGraspZ': <SY.boxGraspZ: 40>, 'lift': <SY.lift: 41>, 'stableYPhi': <SY.stableYPhi: 42>, 'stableOnX': <SY.stableOnX: 43>, 'stableOnY': <SY.stableOnY: 44>, 'end': <SY.end: 46>}
    above: ry.SY # value = <SY.above: 1>
    alignByInt: ry.SY # value = <SY.alignByInt: 31>
    bounce: ry.SY # value = <SY.bounce: 22>
    boxGraspX: ry.SY # value = <SY.boxGraspX: 38>
    boxGraspY: ry.SY # value = <SY.boxGraspY: 39>
    boxGraspZ: ry.SY # value = <SY.boxGraspZ: 40>
    break: ry.SY # value = <SY.break: 17>
    contact: ry.SY # value = <SY.contact: 19>
    contactComplementary: ry.SY # value = <SY.contactComplementary: 21>
    contactStick: ry.SY # value = <SY.contactStick: 20>
    dampMotion: ry.SY # value = <SY.dampMotion: 29>
    downUp: ry.SY # value = <SY.downUp: 16>
    dynamic: ry.SY # value = <SY.dynamic: 11>
    dynamicOn: ry.SY # value = <SY.dynamicOn: 12>
    dynamicTrans: ry.SY # value = <SY.dynamicTrans: 13>
    end: ry.SY # value = <SY.end: 46>
    forceBalance: ry.SY # value = <SY.forceBalance: 33>
    identical: ry.SY # value = <SY.identical: 30>
    inside: ry.SY # value = <SY.inside: 2>
    lift: ry.SY # value = <SY.lift: 41>
    magic: ry.SY # value = <SY.magic: 24>
    magicTrans: ry.SY # value = <SY.magicTrans: 25>
    makeFree: ry.SY # value = <SY.makeFree: 32>
    oppose: ry.SY # value = <SY.oppose: 3>
    poseEq: ry.SY # value = <SY.poseEq: 5>
    positionEq: ry.SY # value = <SY.positionEq: 6>
    push: ry.SY # value = <SY.push: 23>
    pushAndPlace: ry.SY # value = <SY.pushAndPlace: 26>
    quasiStatic: ry.SY # value = <SY.quasiStatic: 14>
    quasiStaticOn: ry.SY # value = <SY.quasiStaticOn: 15>
    relPosY: ry.SY # value = <SY.relPosY: 34>
    restingOn: ry.SY # value = <SY.restingOn: 4>
    stable: ry.SY # value = <SY.stable: 9>
    stableOn: ry.SY # value = <SY.stableOn: 10>
    stableOnX: ry.SY # value = <SY.stableOnX: 43>
    stableOnY: ry.SY # value = <SY.stableOnY: 44>
    stablePose: ry.SY # value = <SY.stablePose: 8>
    stableRelPose: ry.SY # value = <SY.stableRelPose: 7>
    stableYPhi: ry.SY # value = <SY.stableYPhi: 42>
    stableZero: ry.SY # value = <SY.stableZero: 18>
    topBoxGrasp: ry.SY # value = <SY.topBoxGrasp: 27>
    topBoxPlace: ry.SY # value = <SY.topBoxPlace: 28>
    touch: ry.SY # value = <SY.touch: 0>
    touchBoxNormalX: ry.SY # value = <SY.touchBoxNormalX: 35>
    touchBoxNormalY: ry.SY # value = <SY.touchBoxNormalY: 36>
    touchBoxNormalZ: ry.SY # value = <SY.touchBoxNormalZ: 37>
    pass
class Simulation():
    """
    todo doc
    """
    def __init__(self, C: Config, engine: SimulationEngine, verbose: int = 2) -> None: 
        """
        create a Simulation that is associated/attached to the given configuration
        """
    def addImp(self, arg0: ImpType, arg1: StringA, arg2: arr) -> None: ...
    @staticmethod
    def addSensor(*args, **kwargs) -> typing.Any: ...
    def closeGripper(self, gripperFrameName: str, width: float = 0.05, speed: float = 0.3, force: float = 20.0) -> None: ...
    def depthData2pointCloud(self, arg0: numpy.ndarray[numpy.float32], arg1: typing.List[float]) -> numpy.ndarray[numpy.float64]: ...
    def getGripperIsGrasping(self, gripperFrameName: str) -> bool: ...
    def getGripperWidth(self, gripperFrameName: str) -> float: ...
    def getGroundTruthPosition(self, arg0: str) -> numpy.ndarray[numpy.float64]: ...
    def getGroundTruthRotationMatrix(self, arg0: str) -> numpy.ndarray[numpy.float64]: ...
    def getGroundTruthSize(self, arg0: str) -> numpy.ndarray[numpy.float64]: ...
    def getImageAndDepth(self) -> tuple: ...
    @staticmethod
    def getScreenshot(*args, **kwargs) -> typing.Any: ...
    def getState(self) -> tuple: 
        """
        returns a 4-tuple or frame state, joint state, frame velocities (linear & angular), joint velocities
        """
    def getTimeToMove(self) -> float: ...
    def get_q(self) -> arr: ...
    def get_qDot(self) -> arr: ...
    def loadTeleopCallbacks(self) -> None: ...
    def openGripper(self, gripperFrameName: str, width: float = 0.075, speed: float = 0.3) -> None: ...
    def pushConfigurationToSimulator(self, frameVelocities: arr = array(0.0078125), jointVelocities: arr = array(0.0078125)) -> None: 
        """
        set the simulator to the full (frame) state of the configuration
        """
    @staticmethod
    def selectSensor(*args, **kwargs) -> typing.Any: ...
    def setMoveto(self, path: arr, t: float, append: bool = True) -> None: 
        """
        set the spline reference to genreate motion
        """
    def setState(self, frameState: arr, jointState: arr = array(0.0078125), frameVelocities: arr = array(0.0078125), jointVelocities: arr = array(0.0078125)) -> None: ...
    def step(self, u_control: arr, tau: float = 0.01, u_mode: ControlMode = ControlMode.velocity) -> None: ...
    pass
class SimulationEngine():
    """
    Members:

      physx

      bullet

      kinematic
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'physx': <SimulationEngine.physx: 1>, 'bullet': <SimulationEngine.bullet: 2>, 'kinematic': <SimulationEngine.kinematic: 3>}
    bullet: ry.SimulationEngine # value = <SimulationEngine.bullet: 2>
    kinematic: ry.SimulationEngine # value = <SimulationEngine.kinematic: 3>
    physx: ry.SimulationEngine # value = <SimulationEngine.physx: 1>
    pass
class Skeleton():
    def __init__(self) -> None: ...
    def add(self, arg0: list) -> None: ...
    def addEntry(self, timeInterval: arr, symbol: SY, frames: StringA) -> None: ...
    def addExplicitCollisions(self, collisions: StringA) -> None: ...
    def addLiftPriors(self, lift: StringA) -> None: ...
    def enableAccumulatedCollisions(self, enable: bool = True) -> None: ...
    def getKOMO_finalSlice(self, Configuration: Config, lenScale: float, homingScale: float, collScale: float) -> KOMO: ...
    def getKomo_path(self, Configuration: Config, stepsPerPhase: int, accScale: float, lenScale: float, homingScale: float, collScale: float) -> KOMO: ...
    def getKomo_waypoints(self, Configuration: Config, lenScale: float, homingScale: float, collScale: float) -> KOMO: ...
    def getMaxPhase(self) -> float: ...
    def getTwoWaypointProblem(self, t2: int, komoWays: KOMO) -> tuple: ...
    pass
class SolverReturn():
    """
    return of nlp solve call
    """
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    def dict(self) -> dict: ...
    @property
    def done(self) -> bool:
        """
        :type: bool
        """
    @done.setter
    def done(self, arg0: bool) -> None:
        pass
    @property
    def eq(self) -> float:
        """
        :type: float
        """
    @eq.setter
    def eq(self, arg0: float) -> None:
        pass
    @property
    def evals(self) -> int:
        """
        :type: int
        """
    @evals.setter
    def evals(self, arg0: int) -> None:
        pass
    @property
    def f(self) -> float:
        """
        :type: float
        """
    @f.setter
    def f(self, arg0: float) -> None:
        pass
    @property
    def feasible(self) -> bool:
        """
        :type: bool
        """
    @feasible.setter
    def feasible(self, arg0: bool) -> None:
        pass
    @property
    def ineq(self) -> float:
        """
        :type: float
        """
    @ineq.setter
    def ineq(self, arg0: float) -> None:
        pass
    @property
    def sos(self) -> float:
        """
        :type: float
        """
    @sos.setter
    def sos(self, arg0: float) -> None:
        pass
    @property
    def time(self) -> float:
        """
        :type: float
        """
    @time.setter
    def time(self, arg0: float) -> None:
        pass
    @property
    def x(self) -> arr:
        """
        :type: arr
        """
    @x.setter
    def x(self, arg0: arr) -> None:
        pass
    pass
def compiled() -> str:
    """
    return a compile date+time version string
    """
def getStartGoalPath(arg0: Config, arg1: arr, arg2: arr) -> arr:
    pass
def params_add(arg0: dict) -> None:
    """
    add/set parameters
    """
def params_clear() -> None:
    """
    clear all parameters
    """
def params_file(arg0: str) -> None:
    """
    add parameters from a file
    """
def params_print() -> None:
    """
    print the parameters
    """
def raiPath(*args, **kwargs) -> typing.Any:
    """
    get a path relative to rai base path
    """
def setRaiPath(arg0: str) -> None:
    """
    redefine the rai (or rai-robotModels) path
    """
Ceres: ry.NLP_SolverID # value = <NLP_SolverID.Ceres: 10>
Ipopt: ry.NLP_SolverID # value = <NLP_SolverID.Ipopt: 9>
LBFGS: ry.NLP_SolverID # value = <NLP_SolverID.LBFGS: 2>
NLopt: ry.NLP_SolverID # value = <NLP_SolverID.NLopt: 8>
XBall: ry.JT # value = <JT.XBall: 15>
_left: ry.ArgWord # value = <ArgWord._left: 0>
_path: ry.ArgWord # value = <ArgWord._path: 3>
_right: ry.ArgWord # value = <ArgWord._right: 1>
_sequence: ry.ArgWord # value = <ArgWord._sequence: 2>
above: ry.SY # value = <SY.above: 1>
aboveBox: ry.FS # value = <FS.aboveBox: 33>
acceleration: ry.ControlMode # value = <ControlMode.acceleration: 3>
accumulatedCollisions: ry.FS # value = <FS.accumulatedCollisions: 27>
adversarialDropper: ry.ImpType # value = <ImpType.adversarialDropper: 4>
alignByInt: ry.SY # value = <SY.alignByInt: 31>
angularVel: ry.FS # value = <FS.angularVel: 26>
augmentedLag: ry.NLP_SolverID # value = <NLP_SolverID.augmentedLag: 4>
bounce: ry.SY # value = <SY.bounce: 22>
box: ry.ST # value = <ST.box: 0>
boxGraspX: ry.SY # value = <SY.boxGraspX: 38>
boxGraspY: ry.SY # value = <SY.boxGraspY: 39>
boxGraspZ: ry.SY # value = <SY.boxGraspZ: 40>
break: ry.SY # value = <SY.break: 17>
bullet: ry.SimulationEngine # value = <SimulationEngine.bullet: 2>
camera: ry.ST # value = <ST.camera: 12>
capsule: ry.ST # value = <ST.capsule: 2>
closeGripper: ry.ImpType # value = <ImpType.closeGripper: 0>
contact: ry.SY # value = <SY.contact: 19>
contactComplementary: ry.SY # value = <SY.contactComplementary: 21>
contactConstraints: ry.FS # value = <FS.contactConstraints: 42>
contactStick: ry.SY # value = <SY.contactStick: 20>
cylinder: ry.ST # value = <ST.cylinder: 4>
dampMotion: ry.SY # value = <SY.dampMotion: 29>
depthNoise: ry.ImpType # value = <ImpType.depthNoise: 2>
distance: ry.FS # value = <FS.distance: 29>
downUp: ry.SY # value = <SY.downUp: 16>
dynamic: ry.SY # value = <SY.dynamic: 11>
dynamicOn: ry.SY # value = <SY.dynamicOn: 12>
dynamicTrans: ry.SY # value = <SY.dynamicTrans: 13>
end: ry.SY # value = <SY.end: 46>
energy: ry.FS # value = <FS.energy: 43>
eq: ry.OT # value = <OT.eq: 4>
f: ry.OT # value = <OT.f: 1>
forceBalance: ry.SY # value = <SY.forceBalance: 33>
free: ry.JT # value = <JT.free: 16>
gazeAt: ry.FS # value = <FS.gazeAt: 25>
generic: ry.JT # value = <JT.generic: 17>
gradientDescent: ry.NLP_SolverID # value = <NLP_SolverID.gradientDescent: 0>
hingeX: ry.JT # value = <JT.hingeX: 1>
hingeY: ry.JT # value = <JT.hingeY: 2>
hingeZ: ry.JT # value = <JT.hingeZ: 3>
identical: ry.SY # value = <SY.identical: 30>
ineq: ry.OT # value = <OT.ineq: 3>
ineqB: ry.OT # value = <OT.ineqB: 5>
ineqP: ry.OT # value = <OT.ineqP: 6>
inside: ry.SY # value = <SY.inside: 2>
insideBox: ry.FS # value = <FS.insideBox: 34>
jointLimits: ry.FS # value = <FS.jointLimits: 28>
jointState: ry.FS # value = <FS.qItself: 31>
kinematic: ry.SimulationEngine # value = <SimulationEngine.kinematic: 3>
lift: ry.SY # value = <SY.lift: 41>
logBarrier: ry.NLP_SolverID # value = <NLP_SolverID.logBarrier: 6>
magic: ry.SY # value = <SY.magic: 24>
magicTrans: ry.SY # value = <SY.magicTrans: 25>
makeFree: ry.SY # value = <SY.makeFree: 32>
marker: ry.ST # value = <ST.marker: 5>
mesh: ry.ST # value = <ST.mesh: 3>
moveGripper: ry.ImpType # value = <ImpType.moveGripper: 1>
negDistance: ry.FS # value = <FS.distance: 29>
newton: ry.NLP_SolverID # value = <NLP_SolverID.newton: 3>
noPenetrations: ry.ImpType # value = <ImpType.noPenetrations: 7>
none: ry.OT # value = <OT.none: 0>
objectImpulses: ry.ImpType # value = <ImpType.objectImpulses: 5>
oppose: ry.SY # value = <SY.oppose: 3>
pairCollision_negScalar: ry.FS # value = <FS.pairCollision_negScalar: 35>
pairCollision_normal: ry.FS # value = <FS.pairCollision_normal: 37>
pairCollision_p1: ry.FS # value = <FS.pairCollision_p1: 38>
pairCollision_p2: ry.FS # value = <FS.pairCollision_p2: 39>
pairCollision_vector: ry.FS # value = <FS.pairCollision_vector: 36>
phiTransXY: ry.JT # value = <JT.phiTransXY: 14>
physics: ry.FS # value = <FS.physics: 41>
physx: ry.SimulationEngine # value = <SimulationEngine.physx: 1>
pointCloud: ry.ST # value = <ST.pointCloud: 6>
pose: ry.FS # value = <FS.pose: 6>
poseDiff: ry.FS # value = <FS.poseDiff: 7>
poseEq: ry.SY # value = <SY.poseEq: 5>
poseRel: ry.FS # value = <FS.poseRel: 8>
position: ry.ControlMode # value = <ControlMode.position: 1>
positionDiff: ry.FS # value = <FS.positionDiff: 1>
positionEq: ry.SY # value = <SY.positionEq: 6>
positionRel: ry.FS # value = <FS.positionRel: 2>
push: ry.SY # value = <SY.push: 23>
pushAndPlace: ry.SY # value = <SY.pushAndPlace: 26>
qItself: ry.FS # value = <FS.qItself: 31>
quad: ry.ST # value = <ST.quad: 11>
quasiStatic: ry.SY # value = <SY.quasiStatic: 14>
quasiStaticOn: ry.SY # value = <SY.quasiStaticOn: 15>
quatBall: ry.JT # value = <JT.quatBall: 13>
quaternion: ry.FS # value = <FS.quaternion: 3>
quaternionDiff: ry.FS # value = <FS.quaternionDiff: 4>
quaternionRel: ry.FS # value = <FS.quaternionRel: 5>
relPosY: ry.SY # value = <SY.relPosY: 34>
restingOn: ry.SY # value = <SY.restingOn: 4>
rgbNoise: ry.ImpType # value = <ImpType.rgbNoise: 3>
rigid: ry.JT # value = <JT.rigid: 12>
rprop: ry.NLP_SolverID # value = <NLP_SolverID.rprop: 1>
scalarProductXX: ry.FS # value = <FS.scalarProductXX: 18>
scalarProductXY: ry.FS # value = <FS.scalarProductXY: 19>
scalarProductXZ: ry.FS # value = <FS.scalarProductXZ: 20>
scalarProductYX: ry.FS # value = <FS.scalarProductYX: 21>
scalarProductYY: ry.FS # value = <FS.scalarProductYY: 22>
scalarProductYZ: ry.FS # value = <FS.scalarProductYZ: 23>
scalarProductZZ: ry.FS # value = <FS.scalarProductZZ: 24>
sdf: ry.ST # value = <ST.sdf: 13>
singleSquaredPenalty: ry.NLP_SolverID # value = <NLP_SolverID.singleSquaredPenalty: 7>
sos: ry.OT # value = <OT.sos: 2>
sphere: ry.ST # value = <ST.sphere: 1>
spline: ry.ControlMode # value = <ControlMode.spline: 5>
squaredPenalty: ry.NLP_SolverID # value = <NLP_SolverID.squaredPenalty: 5>
ssBox: ry.ST # value = <ST.ssBox: 8>
ssBoxElip: ry.ST # value = <ST.ssBoxElip: 10>
ssCvx: ry.ST # value = <ST.ssCvx: 7>
ssCylinder: ry.ST # value = <ST.ssCylinder: 9>
stable: ry.SY # value = <SY.stable: 9>
stableOn: ry.SY # value = <SY.stableOn: 10>
stableOnX: ry.SY # value = <SY.stableOnX: 43>
stableOnY: ry.SY # value = <SY.stableOnY: 44>
stablePose: ry.SY # value = <SY.stablePose: 8>
stableRelPose: ry.SY # value = <SY.stableRelPose: 7>
stableYPhi: ry.SY # value = <SY.stableYPhi: 42>
stableZero: ry.SY # value = <SY.stableZero: 18>
standingAbove: ry.FS # value = <FS.standingAbove: 40>
tau: ry.JT # value = <JT.tau: 18>
topBoxGrasp: ry.SY # value = <SY.topBoxGrasp: 27>
topBoxPlace: ry.SY # value = <SY.topBoxPlace: 28>
touch: ry.SY # value = <SY.touch: 0>
touchBoxNormalX: ry.SY # value = <SY.touchBoxNormalX: 35>
touchBoxNormalY: ry.SY # value = <SY.touchBoxNormalY: 36>
touchBoxNormalZ: ry.SY # value = <SY.touchBoxNormalZ: 37>
trans3: ry.JT # value = <JT.trans3: 8>
transAccelerations: ry.FS # value = <FS.transAccelerations: 44>
transVelocities: ry.FS # value = <FS.transVelocities: 45>
transX: ry.JT # value = <JT.transX: 4>
transXY: ry.JT # value = <JT.transXY: 7>
transXYPhi: ry.JT # value = <JT.transXYPhi: 9>
transY: ry.JT # value = <JT.transY: 5>
transYPhi: ry.JT # value = <JT.transYPhi: 10>
transZ: ry.JT # value = <JT.transZ: 6>
universal: ry.JT # value = <JT.universal: 11>
vectorX: ry.FS # value = <FS.vectorX: 9>
vectorXDiff: ry.FS # value = <FS.vectorXDiff: 10>
vectorXRel: ry.FS # value = <FS.vectorXRel: 11>
vectorY: ry.FS # value = <FS.vectorY: 12>
vectorYDiff: ry.FS # value = <FS.vectorYDiff: 13>
vectorYRel: ry.FS # value = <FS.vectorYRel: 14>
vectorZ: ry.FS # value = <FS.vectorZ: 15>
vectorZDiff: ry.FS # value = <FS.vectorZDiff: 16>
vectorZRel: ry.FS # value = <FS.vectorZRel: 17>
velocity: ry.ControlMode # value = <ControlMode.velocity: 2>
