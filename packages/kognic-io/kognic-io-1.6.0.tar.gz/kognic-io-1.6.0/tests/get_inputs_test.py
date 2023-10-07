from typing import List

import pytest

import examples.cameras as cameras_example
import examples.get_inputs as get_inputs_example
import examples.get_inputs_by_uuids as get_inputs_by_uuids_example
import kognic.io.client as IOC
import kognic.io.model as IAM
from tests.utils import TestProjects


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestInput:
    @staticmethod
    def filter_cameras_project(projects: List[IAM.Project]):
        return [p for p in projects if p.project == TestProjects.CamerasProject]

    def test_get_inputs_for_project(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects)[0].project
        project_inputs = get_inputs_example.run(client=client, project=project)

        assert isinstance(project_inputs, list)
        assert len(project_inputs) >= 1

    def test_get_inputs_with_uuid(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects)[0].project
        resp = cameras_example.run(client=client, project=project, dryrun=False)
        scene_uuid = resp.scene_uuid

        assert isinstance(scene_uuid, str)

        inputs = get_inputs_by_uuids_example.run(client=client, scene_uuids=[scene_uuid])

        assert isinstance(inputs, list)
        assert len(inputs) == 1
