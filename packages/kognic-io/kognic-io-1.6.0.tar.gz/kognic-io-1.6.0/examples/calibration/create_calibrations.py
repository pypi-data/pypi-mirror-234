import kognic.io.client as IOC
import kognic.io.model as IAM
from examples.calibration.calibration import create_sensor_calibration


def run(client: IOC.KognicIOClient, calibration_identifier: str) -> IAM.SensorCalibrationEntry:
    print("Listing Calibration...")

    lidar_sensor1 = "lidar"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    cam_sensor3 = "RFC03"

    # Create calibration
    calibration_spec = create_sensor_calibration(calibration_identifier, [lidar_sensor1], [cam_sensor1, cam_sensor2, cam_sensor3])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    return created_calibration


if __name__ == "__main__":
    from datetime import datetime

    client = IOC.KognicIOClient()
    calibration_identifier = f"calibration-{datetime.now()}"
    run(client, calibration_identifier)
