from __future__ import absolute_import

import os.path
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.lidars_and_cameras_sequence as LCSM
import kognic.io.model.scene.resources as ResourceModel
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.logger import setup_logging


def run(
    client: IOC.KognicIOClient, project: str, annotation_types: Optional[List[str]] = None, dryrun: bool = True
) -> SceneModel.CreateSceneResponse:
    print("Creating Lidar and Camera Sequence Scene...")

    lidar_sensor1 = "RFL01"
    lidar_sensor2 = "RFL02"
    cam_sensor1 = "RFC01"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicleId": "abg"}
    examples_path = os.path.dirname(__file__)

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1, lidar_sensor2], [cam_sensor1])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    lidars_and_cameras_seq = LCSM.LidarsAndCamerasSequence(
        external_id=f"LCS-with-dropouts-example-{uuid4()}",
        frames=[
            LCSM.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL02.csv", sensor_name=lidar_sensor2),
                ],
                images=[ResourceModel.Image(filename=examples_path + "/resources/img_RFC01.jpg", sensor_name=cam_sensor1)],
            ),
            LCSM.Frame(
                frame_id="2",
                relative_timestamp=100,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL02.csv", sensor_name=lidar_sensor1),
                ],
                images=[ResourceModel.Image(filename=examples_path + "/resources/img_RFC02.jpg", sensor_name=cam_sensor1)],
            ),
            LCSM.Frame(
                frame_id="3",
                relative_timestamp=200,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL11.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL12.csv", sensor_name=lidar_sensor2),
                ],
                images=[ResourceModel.Image(filename=examples_path + "/resources/img_RFC11.jpg", sensor_name=cam_sensor1)],
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )
    # Add input
    return client.lidars_and_cameras_sequence.create(
        lidars_and_cameras_seq, project=project, annotation_types=annotation_types, dryrun=dryrun
    )


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"
    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["annotation-type"]

    run(client, project, annotation_types, dryrun=True)
