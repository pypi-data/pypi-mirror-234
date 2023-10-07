"""Client for communicating with the Kognic platform."""
import logging
from typing import Optional

from deprecated import deprecated
from kognic.auth import DEFAULT_HOST as DEFAULT_AUTH_HOST
from kognic.base_clients.cloud_storage import FileResourceClient
from kognic.base_clients.http_client import HttpClient

from kognic.io.resources.annotation.annotation import AnnotationResource
from kognic.io.resources.calibration.calibration import CalibrationResource
from kognic.io.resources.input.input import InputResource
from kognic.io.resources.pre_annotation.pre_annotation import PreAnnotationResource
from kognic.io.resources.project.project import ProjectResource
from kognic.io.resources.scene.aggregated_lidars_and_cameras_seq import AggregatedLidarsAndCamerasSequence
from kognic.io.resources.scene.cameras import Cameras
from kognic.io.resources.scene.cameras_sequence import CamerasSequence
from kognic.io.resources.scene.lidars import Lidars
from kognic.io.resources.scene.lidars_and_cameras import LidarsAndCameras
from kognic.io.resources.scene.lidars_and_cameras_sequence import LidarsAndCamerasSequence
from kognic.io.resources.scene.lidars_sequence import LidarsSequence
from kognic.io.resources.scene.scene import SceneResource

DEFAULT_HOST = "https://input.app.kognic.com"

log = logging.getLogger(__name__)


class KognicIOClient:
    """Client to work upload and retrieve data from the Kognic platform"""

    def __init__(
        self,
        *,
        auth=None,
        host: str = DEFAULT_HOST,
        auth_host: str = DEFAULT_AUTH_HOST,
        client_organization_id: Optional[int] = None,
        max_retry_attempts: int = 23,
        max_retry_wait_time: int = 60,
        timeout: int = 60,
    ):
        """
        :param auth: auth credentials, see https://developers.kognic.com/docs/kognic-auth
        :param host: override for api url
        :param auth_host: override for authentication url
        :param client_organization_id: Overrides your users organization id. Only works with an Kognic user.
        :param max_upload_retry_attempts: Max number of attempts to retry uploading a file to GCS.
        :param max_upload_retry_wait_time:  Max with time before retrying an upload to GCS.
        :param timeout: Max time to wait for response from server.
        """

        self._client = HttpClient(
            auth=auth,
            host=host,
            auth_host=auth_host,
            client_organization_id=client_organization_id,
            timeout=timeout,
        )
        self._file_client = FileResourceClient(
            max_retry_attempts=max_retry_attempts,
            max_retry_wait_time=max_retry_wait_time,
            timeout=timeout,
        )

        self.calibration = CalibrationResource(self._client, self._file_client)
        self.project = ProjectResource(self._client, self._file_client)
        self.annotation = AnnotationResource(self._client, self._file_client)
        self.input = InputResource(self._client, self._file_client)
        self.pre_annotation = PreAnnotationResource(self._client, self._file_client)
        self.scene = SceneResource(self._client, self._file_client)

        self.lidars_and_cameras = LidarsAndCameras(self._client, self._file_client)
        self.lidars_and_cameras_sequence = LidarsAndCamerasSequence(self._client, self._file_client)
        self.cameras = Cameras(self._client, self._file_client)
        self.cameras_sequence = CamerasSequence(self._client, self._file_client)
        self.lidars = Lidars(self._client, self._file_client)
        self.lidars_sequence = LidarsSequence(self._client, self._file_client)
        self.aggregated_lidars_and_cameras_seq = AggregatedLidarsAndCamerasSequence(self._client, self._file_client)

    @property
    @deprecated(reason="Use `lidars_and_cameras` instead")
    def lidar_and_cameras(self) -> LidarsAndCameras:
        return self.lidars_and_cameras
