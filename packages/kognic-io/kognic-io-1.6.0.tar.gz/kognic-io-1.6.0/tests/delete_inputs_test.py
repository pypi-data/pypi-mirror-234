from __future__ import absolute_import

from typing import List

import pytest

import examples.cameras as cameras_example
import examples.delete_input as delete_input_example
import kognic.io.client as IOC
import kognic.io.model as IAM
from examples.utils import wait_for_scene_job
from kognic.io.model import SceneStatus
from tests.utils import TestProjects


# TODO: Replace me with real method when we have that
def get_inputs_for_scene(client: IOC.KognicIOClient, scene_uuid: str):
    return client.scene._client.get(f"/v1/scenes/{scene_uuid}/inputs")


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestDeleteInput:
    @staticmethod
    def filter_cameras_project(projects: List[IAM.Project]):
        return [p for p in projects if p.project == TestProjects.CamerasProject]

    def test_delete_inputs(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects)[0].project
        scene_response = cameras_example.run(client=client, project=project, dryrun=False)
        scene_uuid = scene_response.scene_uuid

        assert isinstance(scene_uuid, str)
        status = wait_for_scene_job(client=client, scene_uuid=scene_uuid, timeout=60)
        assert status == SceneStatus.Created, f"Scene has not been created, has status {status}"

        inputs_for_scene = get_inputs_for_scene(client=client, scene_uuid=scene_uuid)
        assert len(inputs_for_scene) > 0
        nr_inputs_before = len(inputs_for_scene)

        input_uuid = inputs_for_scene[0]["uuid"]
        delete_input_example.run(client=client, input_uuid=input_uuid)

        inputs_for_scene = get_inputs_for_scene(client=client, scene_uuid=scene_uuid)
        assert len(inputs_for_scene) == nr_inputs_before - 1
