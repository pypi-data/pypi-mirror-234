import time
from typing import List
from uuid import uuid4

import pytest

import examples.cameras as cameras_example
import kognic.io.client as IOC
from examples.utils import wait_for_input_creation, wait_for_input_job
from kognic.io.model import InputStatus
from kognic.io.model.projects import Project
from tests.utils import TestProjects


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestDuplicateInputsValidation:
    """
    Tests that validation of duplication of inputs works correctly
    """

    @staticmethod
    def filter_cameras_project(projects: List[Project]):
        return next(p for p in projects if p.project == TestProjects.CamerasProject)

    def test_sync_validation(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects).project
        external_id = f"duplicate-inputs-sync-validation-{uuid4()}"
        scene = cameras_example.build_scene(external_id=external_id)

        # Create first input
        resp = client.cameras.create(scene, project=project, dryrun=False)
        wait_for_input_creation(client=client, input_uuid=resp.scene_uuid)

        # Create second input
        with pytest.raises(RuntimeError) as excinfo:
            client.cameras.create(scene, project=project, dryrun=False)
        assert "Duplicate inputs for external id" in str(excinfo.value)

    def test_async_validation(self, client: IOC.KognicIOClient):
        projects = client.project.get_projects()
        project = self.filter_cameras_project(projects).project
        external_id = f"duplicate-inputs-async-validation-{uuid4()}"
        scene = cameras_example.build_scene(external_id=external_id)

        # Create both inputs
        resp1 = client.cameras.create(scene, project=project, dryrun=False)
        time.sleep(0.5)  # Enough so that input1 is created before input2, but not enough to trigger sync error
        resp2 = client.cameras.create(scene, project=project, dryrun=False)

        # Wait
        input1 = wait_for_input_job(client=client, input_uuid=resp1.scene_uuid)
        input2 = wait_for_input_job(client=client, input_uuid=resp2.scene_uuid)

        assert input1.status == InputStatus.Created
        assert input2.status == InputStatus.Failed
        assert "Duplicate inputs for external id" in input2.error_message
