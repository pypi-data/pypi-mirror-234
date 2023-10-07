from __future__ import absolute_import

import os.path
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from kognic.openlabel.models import OpenLabelAnnotation

import kognic.io.client as IOC
import kognic.io.model.scene.lidars_and_cameras_sequence as LCSM
import kognic.io.model.scene.resources as ResourceModel
from examples.calibration.calibration import create_sensor_calibration
from examples.utils import wait_for_scene_job
from kognic.io.logger import setup_logging


def run(
    client: IOC.KognicIOClient,
    project: str,
    annotation_types: Optional[List[str]] = None,
    dryrun: bool = True,
    pre_annotation: Optional[OpenLabelAnnotation] = None,
) -> Optional[dict]:
    print("Creating Lidar and Camera Sequence Scene with OpenLabel pre-annotations...")

    lidar_sensor1 = "RFL01"
    lidar_sensor2 = "RFL02"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicleId": "abg"}
    examples_path = os.path.dirname(__file__)

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1, lidar_sensor2], [cam_sensor1, cam_sensor2])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    lidars_and_cameras_seq = LCSM.LidarsAndCamerasSequence(
        external_id=f"LCS-with-pre-annotation-example-{uuid4()}",
        frames=[
            LCSM.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL02.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC01.jpg",
                        sensor_name=cam_sensor1,
                    ),
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC02.jpg",
                        sensor_name=cam_sensor2,
                    ),
                ],
            ),
            LCSM.Frame(
                frame_id="2",
                relative_timestamp=4,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL11.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL12.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC11.jpg",
                        sensor_name=cam_sensor1,
                    ),
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC12.jpg",
                        sensor_name=cam_sensor2,
                    ),
                ],
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    # Create Scene but not input since we don't provide project or batch
    scene_response = client.lidars_and_cameras_sequence.create(lidars_and_cameras_seq, annotation_types=annotation_types, dryrun=dryrun)
    if dryrun:
        return scene_response
    wait_for_scene_job(client=client, scene_uuid=scene_response.scene_uuid)

    # Create some pre-annotations using the OpenLabel model.
    if pre_annotation is not None:
        client.pre_annotation.create(scene_uuid=scene_response.scene_uuid, pre_annotation=pre_annotation, dryrun=dryrun)

    create_input_resp = client.lidars_and_cameras_sequence.create_from_scene(
        scene_uuid=scene_response.scene_uuid, annotation_types=annotation_types, project=project, dryrun=dryrun
    )
    return create_input_resp


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-id>"

    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["<annotation-type>"]

    run(client, project, annotation_types, dryrun=True)
