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
from examples.imu_data.create_imu_data import create_dummy_imu_data
from kognic.io.logger import setup_logging


def run(
    client: IOC.KognicIOClient, project: str, annotation_types: Optional[List[str]] = None, dryrun: bool = True
) -> SceneModel.CreateSceneResponse:
    print("Creating Lidar and Camera Sequence Scene...")

    lidar_sensor1 = "RFL01"
    lidar_sensor2 = "RFL02"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicleId": "abg"}
    examples_path = os.path.dirname(__file__)

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1, lidar_sensor2], [cam_sensor1, cam_sensor2])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    # Generate IMU data
    ONE_MILLISECOND = 1000000  # one millisecond, expressed in nanos
    start_ts = 1648200140000000000
    end_ts = start_ts + 10 * ONE_MILLISECOND
    imu_data = create_dummy_imu_data(start_timestamp=start_ts, end_timestamp=end_ts, samples_per_sec=1000)

    lidars_and_cameras_seq = LCSM.LidarsAndCamerasSequence(
        external_id=f"LCS-full-with-imu-and-shutter-example-{uuid4()}",
        frames=[
            LCSM.Frame(
                frame_id="1",
                unix_timestamp=start_ts + ONE_MILLISECOND,
                relative_timestamp=0,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL02.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC01.jpg",
                        sensor_name=cam_sensor1,
                        metadata=ResourceModel.ImageMetadata(
                            shutter_time_start_ns=start_ts + 0.5 * ONE_MILLISECOND, shutter_time_end_ns=start_ts + 1.5 * ONE_MILLISECOND
                        ),
                    ),
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC02.jpg",
                        sensor_name=cam_sensor2,
                        metadata=ResourceModel.ImageMetadata(
                            shutter_time_start_ns=start_ts + 0.5 * ONE_MILLISECOND, shutter_time_end_ns=start_ts + 1.5 * ONE_MILLISECOND
                        ),
                    ),
                ],
            ),
            LCSM.Frame(
                frame_id="2",
                unix_timestamp=start_ts + 5 * ONE_MILLISECOND,
                relative_timestamp=4,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL11.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL12.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC11.jpg",
                        sensor_name=cam_sensor1,
                        metadata=ResourceModel.ImageMetadata(
                            shutter_time_start_ns=start_ts + 4.5 * ONE_MILLISECOND, shutter_time_end_ns=start_ts + 5.5 * ONE_MILLISECOND
                        ),
                    ),
                    ResourceModel.Image(
                        filename=examples_path + "/resources/img_RFC12.jpg",
                        sensor_name=cam_sensor2,
                        metadata=ResourceModel.ImageMetadata(
                            shutter_time_start_ns=start_ts + 4.5 * ONE_MILLISECOND, shutter_time_end_ns=start_ts + 5.5 * ONE_MILLISECOND
                        ),
                    ),
                ],
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
        imu_data=imu_data,
    )
    # Add input
    return client.lidars_and_cameras_sequence.create(
        lidars_and_cameras_seq, project=project, annotation_types=annotation_types, dryrun=dryrun
    )


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-id>"
    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["<annotation-type>"]

    run(client, project, annotation_types, dryrun=True)
