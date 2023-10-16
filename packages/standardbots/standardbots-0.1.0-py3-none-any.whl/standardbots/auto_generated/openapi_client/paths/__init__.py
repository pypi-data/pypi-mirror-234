# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from standardbots.auto_generated.openapi_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_HEALTH = "/api/v1/health"
    API_V1_CONTROL_POSITION = "/api/v1/control/position"
    API_V1_CONTROL_BRAKES = "/api/v1/control/brakes"
    API_V1_CONTROL_EMERGENCYSTOP = "/api/v1/control/emergency-stop"
    API_V1_CONTROL_DEVICES_GRIPPER = "/api/v1/control/devices/gripper"
    API_V1_CAMERAS = "/api/v1/cameras"
    API_V1_CAMERAS_CAMERA_ID_FRAME_RGB = "/api/v1/cameras/{cameraId}/frame/rgb"
    API_V1_CONFIGURATION_CONTROLMODE = "/api/v1/configuration/control-mode"
    API_V1_CONFIGURATION_DEVICES_GRIPPER = "/api/v1/configuration/devices/gripper"
    API_V1_ROUTINEEDITOR_ROUTINES = "/api/v1/routine-editor/routines"
    API_V1_ROUTINEEDITOR_ROUTINES_ROUTINE_ID = "/api/v1/routine-editor/routines/{routineId}"
    API_V1_ROUTINEEDITOR_RUNTIME_VARIABLES_VARIABLE_ID = "/api/v1/routine-editor/runtime/variables/{variableId}"
