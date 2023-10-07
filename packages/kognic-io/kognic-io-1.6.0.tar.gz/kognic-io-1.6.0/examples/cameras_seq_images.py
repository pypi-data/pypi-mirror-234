from __future__ import absolute_import

from typing import List, Optional
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.cameras_sequence as CamerasSeqModel
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData


def run(client: IOC.KognicIOClient, project: str, annotation_types: Optional[List[str]] = None, dryrun: bool = True):
    print("Creating Cameras Sequence Scene...")

    sensor1 = "RFC01"
    sensor2 = "RFC02"
    metadata = MetaData.parse_obj({"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    cameras_sequence = CamerasSeqModel.CamerasSequence(
        external_id=f"camera-seq-images-example-{uuid4()}",
        frames=[
            CamerasSeqModel.Frame(
                frame_id="1",
                relative_timestamp=0,
                images=[
                    # JPG Images in Frame 1
                    SceneModel.Image(filename="./examples/resources/img_RFC01.jpg", sensor_name=sensor1),
                    SceneModel.Image(filename="./examples/resources/img_RFC02.jpg", sensor_name=sensor2),
                ],
                metadata={"dut_status": "active"},
            ),
            CamerasSeqModel.Frame(
                frame_id="2",
                relative_timestamp=500,
                images=[
                    # PNG Images in Frame 2
                    SceneModel.Image(filename="./examples/resources/img_RFC11.png", sensor_name=sensor1),
                    SceneModel.Image(filename="./examples/resources/img_RFC12.png", sensor_name=sensor2),
                ],
                metadata={"dut_status": "active"},
            ),
            CamerasSeqModel.Frame(
                frame_id="3",
                relative_timestamp=1000,
                images=[
                    # WebP VP8 Images in Frame 3
                    SceneModel.Image(filename="./examples/resources/img_RFC21.webp", sensor_name=sensor1),
                    SceneModel.Image(filename="./examples/resources/img_RFC22.webp", sensor_name=sensor2),
                ],
                metadata={"dut_status": "active"},
            ),
            CamerasSeqModel.Frame(
                frame_id="4",
                relative_timestamp=1500,
                images=[
                    # WebP VP8L Images in Frame 4
                    SceneModel.Image(filename="./examples/resources/img_RFC31.webp", sensor_name=sensor1),
                    SceneModel.Image(filename="./examples/resources/img_RFC32.webp", sensor_name=sensor2),
                ],
                metadata={"dut_status": "active"},
            ),
            CamerasSeqModel.Frame(
                frame_id="5",
                relative_timestamp=2000,
                images=[
                    # WebP VP8X Images in Frame 5
                    SceneModel.Image(filename="./examples/resources/img_RFC41.webp", sensor_name=sensor1),
                    SceneModel.Image(filename="./examples/resources/img_RFC42.webp", sensor_name=sensor2),
                ],
                metadata={"dut_status": "active"},
            ),
        ],
        metadata=metadata,
    )

    # Add input
    return client.cameras_sequence.create(cameras_sequence, project=project, annotation_types=annotation_types, dryrun=dryrun)


if __name__ == "__main__":
    setup_logging(level="INFO")
    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"

    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["annotation-type"]

    client = IOC.KognicIOClient()
    run(client, project, annotation_types)
