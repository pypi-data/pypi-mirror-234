from __future__ import absolute_import

import pytest

import examples.lidars_and_cameras_seq as lidars_cameras_seq_example
import kognic.io.client as IOC


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestLidarsAndCamerasSeq:
    def test_create_only_scene_lidars_and_cameras_seq(self, client: IOC.KognicIOClient):
        resp = lidars_cameras_seq_example.run(client=client, project=None, dryrun=False)
        if resp is not None:
            assert isinstance(resp.scene_uuid, str)
        else:
            assert False

        with pytest.raises(AttributeError):
            resp.files
