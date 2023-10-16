# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from standardbots.auto_generated.openapi_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ROBOT__CONFIGURATION = "Robot → Configuration"
    ROBOT__CONTROL = "Robot → Control"
    ROBOT__ROUTINE_EDITOR = "Robot → Routine Editor"
    CAMERAS = "Cameras"
