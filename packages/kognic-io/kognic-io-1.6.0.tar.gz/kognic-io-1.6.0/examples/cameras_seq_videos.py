from __future__ import absolute_import

from typing import Optional
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.cameras_sequence as CamerasSeqModel
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData


def run(client: IOC.KognicIOClient, project: Optional[str], dryrun: bool = True):
    print("Creating Cameras Sequence Scene...")

    sensor1 = "RFC01"
    sensor2 = "RFC02"
    metadata = MetaData.parse_obj({"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    cameras_sequence = CamerasSeqModel.CamerasSequence(
        external_id=f"camera-seq-videos-example-{uuid4()}",
        frames=[
            CamerasSeqModel.Frame(
                frame_id="1",
                relative_timestamp=0,
                video_frames=[
                    SceneModel.VideoFrame(filename="./examples/resources/video_RFC01.mp4", sensor_name=sensor1, video_timestamp=0),
                    SceneModel.VideoFrame(filename="./examples/resources/video_RFC02.mp4", sensor_name=sensor2, video_timestamp=0),
                ],
            ),
            CamerasSeqModel.Frame(
                frame_id="2",
                relative_timestamp=500,
                video_frames=[
                    SceneModel.VideoFrame(filename="./examples/resources/video_RFC01.mp4", sensor_name=sensor1, video_timestamp=100),
                    SceneModel.VideoFrame(filename="./examples/resources/video_RFC02.mp4", sensor_name=sensor2, video_timestamp=100),
                ],
                metadata={"dut_status": "active"},
            ),
        ],
        metadata=metadata,
    )

    # Add input
    return client.cameras_sequence.create(cameras_sequence, project=project, dryrun=dryrun)


if __name__ == "__main__":
    setup_logging(level="INFO")

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"

    client = IOC.KognicIOClient()
    run(client, project)
