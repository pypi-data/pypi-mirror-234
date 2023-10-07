from typing import List

import kognic.io.client as IOC
import kognic.io.model as IAM


def run(client: IOC.KognicIOClient) -> List[IAM.SensorCalibrationEntry]:
    print("Get One Calibration...")

    calibrations = client.calibration.get_calibrations()
    calibration = client.calibration.get_calibrations(external_id=calibrations[0].external_id)

    return calibration


if __name__ == "__main__":
    client = IOC.KognicIOClient()
    run(client)
