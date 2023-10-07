from typing import List

import kognic.io.client as IOC
from kognic.io.model import Scene


def run(client: IOC.KognicIOClient, scene_uuids: List[str]) -> List[Scene]:
    print("Listing scenes...")
    return client.scene.get_scenes_by_uuids(scene_uuids=scene_uuids)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    scene_uuids = ["scene-identifier"]
    run(client, scene_uuids)
