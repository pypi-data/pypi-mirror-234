import typing_extensions

from standardbots.auto_generated.openapi_client.paths import PathValues
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_health import ApiV1Health
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_control_position import ApiV1ControlPosition
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_control_brakes import ApiV1ControlBrakes
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_control_emergency_stop import ApiV1ControlEmergencyStop
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_control_devices_gripper import ApiV1ControlDevicesGripper
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_cameras import ApiV1Cameras
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_cameras_camera_id_frame_rgb import ApiV1CamerasCameraIdFrameRgb
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_configuration_control_mode import ApiV1ConfigurationControlMode
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_configuration_devices_gripper import ApiV1ConfigurationDevicesGripper
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_routine_editor_routines import ApiV1RoutineEditorRoutines
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_routine_editor_routines_routine_id import ApiV1RoutineEditorRoutinesRoutineId
from standardbots.auto_generated.openapi_client.apis.paths.api_v1_routine_editor_runtime_variables_variable_id import ApiV1RoutineEditorRuntimeVariablesVariableId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_HEALTH: ApiV1Health,
        PathValues.API_V1_CONTROL_POSITION: ApiV1ControlPosition,
        PathValues.API_V1_CONTROL_BRAKES: ApiV1ControlBrakes,
        PathValues.API_V1_CONTROL_EMERGENCYSTOP: ApiV1ControlEmergencyStop,
        PathValues.API_V1_CONTROL_DEVICES_GRIPPER: ApiV1ControlDevicesGripper,
        PathValues.API_V1_CAMERAS: ApiV1Cameras,
        PathValues.API_V1_CAMERAS_CAMERA_ID_FRAME_RGB: ApiV1CamerasCameraIdFrameRgb,
        PathValues.API_V1_CONFIGURATION_CONTROLMODE: ApiV1ConfigurationControlMode,
        PathValues.API_V1_CONFIGURATION_DEVICES_GRIPPER: ApiV1ConfigurationDevicesGripper,
        PathValues.API_V1_ROUTINEEDITOR_ROUTINES: ApiV1RoutineEditorRoutines,
        PathValues.API_V1_ROUTINEEDITOR_ROUTINES_ROUTINE_ID: ApiV1RoutineEditorRoutinesRoutineId,
        PathValues.API_V1_ROUTINEEDITOR_RUNTIME_VARIABLES_VARIABLE_ID: ApiV1RoutineEditorRuntimeVariablesVariableId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_HEALTH: ApiV1Health,
        PathValues.API_V1_CONTROL_POSITION: ApiV1ControlPosition,
        PathValues.API_V1_CONTROL_BRAKES: ApiV1ControlBrakes,
        PathValues.API_V1_CONTROL_EMERGENCYSTOP: ApiV1ControlEmergencyStop,
        PathValues.API_V1_CONTROL_DEVICES_GRIPPER: ApiV1ControlDevicesGripper,
        PathValues.API_V1_CAMERAS: ApiV1Cameras,
        PathValues.API_V1_CAMERAS_CAMERA_ID_FRAME_RGB: ApiV1CamerasCameraIdFrameRgb,
        PathValues.API_V1_CONFIGURATION_CONTROLMODE: ApiV1ConfigurationControlMode,
        PathValues.API_V1_CONFIGURATION_DEVICES_GRIPPER: ApiV1ConfigurationDevicesGripper,
        PathValues.API_V1_ROUTINEEDITOR_ROUTINES: ApiV1RoutineEditorRoutines,
        PathValues.API_V1_ROUTINEEDITOR_ROUTINES_ROUTINE_ID: ApiV1RoutineEditorRoutinesRoutineId,
        PathValues.API_V1_ROUTINEEDITOR_RUNTIME_VARIABLES_VARIABLE_ID: ApiV1RoutineEditorRuntimeVariablesVariableId,
    }
)
