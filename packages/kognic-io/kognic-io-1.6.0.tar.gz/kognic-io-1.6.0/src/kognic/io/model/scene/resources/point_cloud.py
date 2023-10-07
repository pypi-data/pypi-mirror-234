from pydantic import validator

from kognic.io.model.scene.resources.resource import Resource
from kognic.io.resources.scene.file_data import FileData

lidar_sensor_default = "lidar"


class PointCloud(Resource):
    sensor_name: str = lidar_sensor_default

    @validator("file_data", pre=True)
    def format_check(cls, value: FileData):
        if not value.format.is_pointcloud:
            raise ValueError(f"Invalid format for pointcloud data: {value.format}")
        return value
