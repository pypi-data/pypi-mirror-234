import time

from kognic.io.client import KognicIOClient
from kognic.io.model import Input, InputStatus, SceneStatus


def wait_for_input_creation(client: KognicIOClient, scene_uuid: str, timeout=20):
    input = wait_for_input_job(client, scene_uuid, timeout)
    if input.status == InputStatus.Created:
        return
    elif input.status == InputStatus.Failed:
        raise Exception(f'Input creation failed for scene uuid {scene_uuid} with error "{input.error_message}"')


def wait_for_input_job(client: KognicIOClient, scene_uuid: str, timeout=20) -> Input:
    wait_for_scene_job(client, scene_uuid, timeout)
    response = client.input.get_inputs_by_uuids(scene_uuids=[scene_uuid])
    if not response:
        raise Exception(f"No input found with scene uuid {scene_uuid}")
    return response[0]


def wait_for_scene_job(client: KognicIOClient, scene_uuid: str, timeout=20) -> SceneStatus:
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        response = client.scene.get_scenes_by_uuids(scene_uuids=[scene_uuid])
        scene = response[0]
        if scene.status in [SceneStatus.Created, SceneStatus.Failed]:
            return scene.status

        time.sleep(1)

    raise Exception(f"Job was not finished: {scene_uuid}")
