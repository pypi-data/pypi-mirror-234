from __future__ import absolute_import

import os.path
from datetime import datetime
from typing import Generator, List, Optional
from uuid import uuid4

import kognic.openlabel.models as OLA

import kognic.io.client as IOC
import kognic.io.model.scene.lidars_and_cameras_sequence as LCS
import kognic.io.model.scene.resources as ResourceModel
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.logger import setup_logging
from kognic.io.tools.input_creation import InputCreationResult, SceneWithPreAnnotation, create_inputs


def run(
    client: IOC.KognicIOClient,
    project: str,
    annotation_types: Optional[List[str]] = None,
    dryrun: bool = True,
    include_preannotations: bool = True,
) -> Generator[InputCreationResult, None, None]:
    with_without = "with" if include_preannotations else "without"
    print(f"Creating Lidar and Camera Input {with_without} pre-annotations...")

    lidar_sensor1 = "RFL01"
    lidar_sensor2 = "RFL02"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicleId": "abg"}
    examples_path = os.path.dirname(__file__)

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1, lidar_sensor2], [cam_sensor1, cam_sensor2])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    lidars_and_cameras_1 = LCS.LidarsAndCamerasSequence(
        external_id=f"LCS-with-pre-annotation-example-{uuid4()}",
        frames=[
            LCS.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL02.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(filename=examples_path + "/resources/img_RFC01.jpg", sensor_name=cam_sensor1),
                    ResourceModel.Image(filename=examples_path + "/resources/img_RFC02.jpg", sensor_name=cam_sensor2),
                ],
            )
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )
    lidars_and_cameras_2 = LCS.LidarsAndCamerasSequence(
        external_id=f"LCS-with-pre-annotation-example-{uuid4()}",
        frames=[
            LCS.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL11.csv", sensor_name=lidar_sensor1),
                    ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL12.csv", sensor_name=lidar_sensor2),
                ],
                images=[
                    ResourceModel.Image(filename=examples_path + "/resources/img_RFC11.jpg", sensor_name=cam_sensor1),
                    ResourceModel.Image(filename=examples_path + "/resources/img_RFC12.jpg", sensor_name=cam_sensor2),
                ],
            )
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    object_1 = OLA.Objects(
        object_data=OLA.ObjectData(
            cuboid=[
                OLA.Cuboid(
                    attributes=OLA.Attributes(text=[OLA.Text(name="stream", val=lidar_sensor1)]),
                    name="cuboid-1",
                    val=[0, 0, 0, 0, -0.7071067811865476, 0.7071067811865476, 0, 1, 1, 1],
                )
            ]
        )
    )
    object_uuid_1 = str(uuid4())
    pre_annotation_1 = OLA.OpenLabelAnnotation(
        openlabel=OLA.Openlabel(
            frame_intervals=[],
            frames={
                "0": OLA.Frame(
                    frame_properties=OLA.FrameProperties(
                        streams={lidar_sensor1: {}, lidar_sensor2: {}, cam_sensor1: {}, cam_sensor2: {}}, timestamp=0, external_id="1"
                    ),
                    objects={object_uuid_1: object_1},
                )
            },
            objects={object_uuid_1: OLA.Object(name=object_uuid_1, type="SpaceShip", object_data=OLA.ObjectData())},
            metadata=OLA.Metadata(schema_version="1.0.0"),
            streams={
                lidar_sensor1: OLA.Stream(type=OLA.StreamTypes.lidar),
                lidar_sensor2: OLA.Stream(type=OLA.StreamTypes.lidar),
                cam_sensor1: OLA.Stream(type=OLA.StreamTypes.camera),
                cam_sensor2: OLA.Stream(type=OLA.StreamTypes.camera),
            },
        )
    )

    object_2 = OLA.Objects(
        object_data=OLA.ObjectData(
            cuboid=[
                OLA.Cuboid(
                    attributes=OLA.Attributes(text=[OLA.Text(name="stream", val=lidar_sensor1)]),
                    name="cuboid-1",
                    val=[0, 0, 0, 0, -0.7071067811865476, 0.7071067811865476, 0, 1, 1, 1],
                )
            ]
        )
    )
    object_uuid_2 = str(uuid4())
    pre_annotation_2 = OLA.OpenLabelAnnotation(
        openlabel=OLA.Openlabel(
            frame_intervals=[],
            frames={
                "0": OLA.Frame(
                    frame_properties=OLA.FrameProperties(
                        streams={lidar_sensor1: {}, lidar_sensor2: {}, cam_sensor1: {}, cam_sensor2: {}}, timestamp=0, external_id="1"
                    ),
                    objects={object_uuid_2: object_2},
                )
            },
            objects={object_uuid_2: OLA.Object(name=object_uuid_2, type="SpaceShip", object_data=OLA.ObjectData())},
            metadata=OLA.Metadata(schema_version="1.0.0"),
            streams={
                lidar_sensor1: OLA.Stream(type=OLA.StreamTypes.lidar),
                lidar_sensor2: OLA.Stream(type=OLA.StreamTypes.lidar),
                cam_sensor1: OLA.Stream(type=OLA.StreamTypes.camera),
                cam_sensor2: OLA.Stream(type=OLA.StreamTypes.camera),
            },
        )
    )

    scenes = [
        SceneWithPreAnnotation(scene=lidars_and_cameras_1, pre_annotation=pre_annotation_1 if include_preannotations else None),
        SceneWithPreAnnotation(scene=lidars_and_cameras_2, pre_annotation=pre_annotation_2 if include_preannotations else None),
    ]

    yield from create_inputs(
        client=client, scenes_with_pre_annotations=scenes, project=project, annotation_types=annotation_types, dryrun=dryrun
    )


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-id>"

    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["<annotation-type>"]

    run(client, project, annotation_types, dryrun=True)
