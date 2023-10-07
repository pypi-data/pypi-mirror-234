from __future__ import absolute_import

from pathlib import Path
from typing import List, Optional
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.cameras as CamerasModel
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData

base_dir = Path(__file__).parent.absolute()


def run(
    client: IOC.KognicIOClient, project: str, annotation_types: Optional[List[str]] = None, dryrun: bool = True
) -> Optional[SceneModel.CreateSceneResponse]:
    print("Creating Cameras Input...")
    cameras = build_scene(external_id=f"cameras-example-{uuid4()}")

    # Add input
    return client.cameras.create(cameras, project=project, annotation_types=annotation_types, dryrun=dryrun)


def build_scene(external_id: str) -> CamerasModel.Cameras:
    sensor1 = "RFC01"
    sensor2 = "RFC02"
    metadata = MetaData.parse_obj({"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    return CamerasModel.Cameras(
        external_id=external_id,
        frame=CamerasModel.Frame(
            images=[
                SceneModel.Image(filename=str(base_dir) + "/resources/img_RFC01.jpg", sensor_name=sensor1),
                SceneModel.Image(filename=str(base_dir) + "/resources/img_RFC02.jpg", sensor_name=sensor2),
            ]
        ),
        metadata=metadata,
    )


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "Project-identifier"
    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["annotation-type"]

    run(client, project, annotation_types)
