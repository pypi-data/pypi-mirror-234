from __future__ import absolute_import

from typing import List

import pytest
from click.testing import CliRunner

import examples.calibration.create_calibrations as calibration_example
import kognic.io.client as IOC
import kognic.io.kognicutil as kognicutil
import kognic.io.model as IAM
from tests.utils import TestProjects


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestKognicUtils:
    @staticmethod
    def filter_lidar_and_cameras_project(projects: List[IAM.Project]):
        return [p for p in projects if p.project == TestProjects.LidarsAndCamerasProject]

    def test_kognicutil_projects(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(kognicutil.projects, obj={"client": client})
        assert result.exit_code == 0, result.output

    def test_kognicutil_projects_specific(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(kognicutil.projects, ["lidars_and_cameras-project"], obj={"client": client})
        assert result.exit_code == 0, result.output

    def test_kognicutil_projects_get_batches(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(kognicutil.projects, ["lidars_and_cameras-project", "--get-batches"], obj={"client": client})
        assert result.exit_code == 0, result.output

    def test_kognicutil_inputs(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(
            kognicutil.inputs,
            ["--project", "lidars_and_cameras-project", "--external-ids", "input1", "--include-invalidated"],
            obj={"client": client},
        )
        assert result.exit_code == 0, result.output

    def test_kognicutil_inputs_view(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(
            kognicutil.inputs,
            ["--project", "lidars_and_cameras-project", "--external-ids", "input1", "--include-invalidated", "--view"],
            obj={"client": client},
        )
        assert result.exit_code == 0, result.output

    def test_kognicutil_view(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(kognicutil.view, ["50bcca91-ac11-423d-b698-f359aefa4da5"], obj={"client": client})
        assert result.exit_code == 0, result.output

    def test_kognicutil_calibration(self, client: IOC.KognicIOClient):
        runner = CliRunner()
        result = runner.invoke(kognicutil.calibration, obj={"client": client})
        assert result.exit_code == 0, result.output

    def test_kognicutil_calibration_external_id(self, client: IOC.KognicIOClient):
        external_id = "the_external_id"
        try:  # Try creating calibration if it doesn't exist
            calibration_example.run(client, external_id)
        except Exception:  # pylint: disable=broad-except
            pass  # Calibration already exists
        runner = CliRunner()
        result = runner.invoke(kognicutil.calibration, ["--external-id", external_id], obj={"client": client})
        assert result.exit_code == 0, result.output
