import kognic.io.client as IOC
import kognic.io.model as IAM


def run(client: IOC.KognicIOClient, scene_uuid: str, reason: IAM.SceneInvalidatedReason) -> None:
    print("Invalidating scenes...")
    return client.scene.invalidate_scenes(scene_uuids=[scene_uuid], reason=reason)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    scene_uuid = "Scene-identifier"
    invalidated_reason = IAM.SceneInvalidatedReason.INCORRECTLY_CREATED
    run(client, scene_uuid, invalidated_reason)
