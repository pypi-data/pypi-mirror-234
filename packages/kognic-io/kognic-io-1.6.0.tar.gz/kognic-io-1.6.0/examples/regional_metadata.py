from __future__ import absolute_import

from pathlib import Path
from uuid import uuid4

import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.cameras as CamerasModel
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData

base_dir = Path(__file__).parent.absolute()


def run() -> CamerasModel.Cameras:
    print("Creating Cameras Scene with MetaDataContainer")

    sensor1 = "RFC01"
    sensor2 = "RFC02"

    # A MetaData container can be created by parsing a dictionary
    metadata = MetaData.parse_obj({"region": "EU", "location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    # It can also be created by initializing with keywords.
    metadata = MetaData(region="EU", location_lat=27.986065, location_long=86.922623, vehicle_id="abg")

    cameras = CamerasModel.Cameras(
        external_id=f"regional-metadata-example-{uuid4()}",
        frame=CamerasModel.Frame(
            images=[
                SceneModel.Image(filename=str(base_dir) + "/resources/img_RFC01.jpg", sensor_name=sensor1),
                SceneModel.Image(filename=str(base_dir) + "/resources/img_RFC02.jpg", sensor_name=sensor2),
            ]
        ),
        metadata=metadata,
    )

    return cameras


if __name__ == "__main__":
    setup_logging(level="INFO")
    print(run())
