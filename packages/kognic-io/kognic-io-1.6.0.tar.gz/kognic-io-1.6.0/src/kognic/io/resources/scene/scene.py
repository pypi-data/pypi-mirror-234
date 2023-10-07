import logging
from typing import List

from kognic.io.model import Scene, SceneInvalidatedReason
from kognic.io.resources.abstract import IOResource

log = logging.getLogger(__name__)


class SceneResource(IOResource):
    """
    Resource exposing Kognic Scenes
    """

    def get_scenes_by_uuids(self, scene_uuids: List[str]) -> List[Scene]:
        """
        Gets scenes using scene uuids. A NotFound exception will be raised if any of the scenes doesn't exist.

        :param scene_uuids: A UUID to filter scenes on
        :return List: List of Scenes
        """

        body = dict(sceneUuids=scene_uuids)
        json_resp = self._client.post("v2/scenes/query", json=body)
        return [Scene.from_json(js) for js in json_resp]

    def invalidate_scenes(self, scene_uuids: List[str], reason: SceneInvalidatedReason) -> None:
        """
        Invalidates scenes. This is a destructive operation, and it's important to be aware of the consequences.
        Read more about it here:
            https://developers.kognic.com/docs/kognic-io/working_with_scenes_and_inputs#invalidate-scenes

        :param scene_uuids: The scene uuids to invalidate
        :param reason: The reason for invalidating the scene
        """
        body = dict(sceneUuids=scene_uuids, reason=reason.value)
        self._client.post("v2/scenes/actions/invalidate", json=body, discard_response=True)
