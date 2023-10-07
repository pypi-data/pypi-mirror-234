from __future__ import absolute_import

import time
from typing import List

import pytest

import examples.cameras as cameras_example
import examples.get_scenes_by_uuids as get_scenes_example
import examples.invalidate_scenes as invalidate_inputs_example
import kognic.io.client as IOC
import kognic.io.model as IAM
from examples.utils import wait_for_scene_job
from kognic.io.model import SceneInvalidatedReason, SceneStatus
from tests.utils import TestProjects

from .delete_inputs_test import get_inputs_for_scene


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestInvalidateScenes:
    @staticmethod
    def filter_cameras_project(projects: List[IAM.Project]):
        return [p for p in projects if p.project == TestProjects.CamerasProject]

    def test_invalidate_scenes(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects)[0].project
        scene_response = cameras_example.run(client=client, project=project, dryrun=False)
        scene_uuid = scene_response.scene_uuid

        assert isinstance(scene_uuid, str)
        status = wait_for_scene_job(client=client, scene_uuid=scene_uuid, timeout=60)
        assert status == SceneStatus.Created, f"Scene has not been created, has status {status}"

        invalidate_inputs_example.run(client=client, scene_uuid=scene_uuid, reason=SceneInvalidatedReason.BAD_CONTENT)

        # TODO: Uncomment this and remove check below once we actually invalidate scenes
        # scenes = get_scenes_example.run(client=client, scene_uuids=[scene_uuid])
        # assert scenes[0].status == "invalidated:broken-input"
        inputs_for_scene = list()
        for i in range(3):
            inputs_for_scene = get_inputs_for_scene(client=client, scene_uuid=scene_uuid)
            if len(inputs_for_scene) == 0:
                break
            time.sleep(1)

        assert len(inputs_for_scene) == 0
