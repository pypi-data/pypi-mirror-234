import typing_extensions

from standardbots.auto_generated.openapi_client.apis.tags import TagValues
from standardbots.auto_generated.openapi_client.apis.tags.robot_configuration_api import RobotConfigurationApi
from standardbots.auto_generated.openapi_client.apis.tags.robot_control_api import RobotControlApi
from standardbots.auto_generated.openapi_client.apis.tags.robot_routine_editor_api import RobotRoutineEditorApi
from standardbots.auto_generated.openapi_client.apis.tags.cameras_api import CamerasApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ROBOT__CONFIGURATION: RobotConfigurationApi,
        TagValues.ROBOT__CONTROL: RobotControlApi,
        TagValues.ROBOT__ROUTINE_EDITOR: RobotRoutineEditorApi,
        TagValues.CAMERAS: CamerasApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ROBOT__CONFIGURATION: RobotConfigurationApi,
        TagValues.ROBOT__CONTROL: RobotControlApi,
        TagValues.ROBOT__ROUTINE_EDITOR: RobotRoutineEditorApi,
        TagValues.CAMERAS: CamerasApi,
    }
)
