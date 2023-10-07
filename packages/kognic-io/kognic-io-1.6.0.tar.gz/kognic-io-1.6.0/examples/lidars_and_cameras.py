from __future__ import absolute_import

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.lidars_and_cameras as LC
import kognic.io.model.scene.resources as ResourceModel
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData


def run(
    client: IOC.KognicIOClient, project: Optional[str], annotation_types: Optional[List[str]] = None, dryrun: bool = True
) -> SceneModel.CreateSceneResponse:
    annotation_types = annotation_types or []
    print("Creating Lidars And Cameras Scene...")

    lidar_sensor1 = "lidar"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    cam_sensor3 = "RFC03"
    metadata = MetaData.parse_obj({"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1], [cam_sensor1, cam_sensor2, cam_sensor3])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    lidars_and_cameras = LC.LidarsAndCameras(
        external_id=f"lidars-and-cameras-example-{uuid4()}",
        frame=LC.Frame(
            point_clouds=[ResourceModel.PointCloud(filename="./examples/resources/point_cloud_RFL01.las", sensor_name=lidar_sensor1)],
            images=[
                ResourceModel.Image(filename="./examples/resources/img_RFC01.jpg", sensor_name=cam_sensor1),
                ResourceModel.Image(filename="./examples/resources/img_RFC02.jpg", sensor_name=cam_sensor2),
            ],
        ),
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    # Add input
    return client.lidars_and_cameras.create(lidars_and_cameras, project=project, annotation_types=annotation_types, dryrun=dryrun)


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"
    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["annotation-type"]

    run(client, project, annotation_types)
