from contextlib import contextmanager
from collections.abc import Generator

from standardbots.auto_generated.openapi_client import models
from standardbots.auto_generated.openapi_client import ApiClient, Configuration
from standardbots.auto_generated.openapi_client.apis.tags import robot_configuration_api, robot_control_api, cameras_api, robot_routine_editor_api

class ControlApi(robot_control_api.RobotControlApi):
  def brake(self, state: str):
    return self.set_brakes_state(body=robot_control_api.ControlBrakesRequest(state='engaged'))
  
  def unbrake(self):
    return self.set_brakes_state(body=robot_control_api.ControlBrakesRequest(state='disengaged'))

  def move(self, **kwargs: models.MoveRequest):
    return self.set_arm_position(body=models.MoveRequest(**kwargs))

  def grip(self, **kwargs: models.GripperCommandRequest):
    return self.control_gripper(body=models.GripperCommandRequest(**kwargs))

class CamerasApi(cameras_api.CamerasApi):
  pass

class ConfigurationApi(robot_configuration_api.RobotConfigurationApi):
  pass

class RoutineEditorApi(robot_routine_editor_api.RobotRoutineEditorApi):
  pass

class StandardBotsSdk:
  def __init__(self, endpoint: str, token: str, robot_kind: str):
    self.endpoint = endpoint
    self.token = token
    self.robot_kind = robot_kind
    self.hello = 'world'

    self.client = self.get_client()
    self.control = ControlApi(self.client)
    self.cameras = CamerasApi(self.client)
    self.configuration = ConfigurationApi(self.client)
    self.routine_editor = RoutineEditorApi(self.client)

  @contextmanager
  def connection(self):
    try:
      yield self
    finally:
      self.close()
  
  def close(self):
    self.client.close()

  def get_client(self) -> ApiClient:
    configuration = Configuration(
      host=self.endpoint,
    )
    configuration.proxy_headers={'robot_kind': self.robot_kind}
    configuration.api_key['token'] = self.token
    return ApiClient(configuration)
