from typing import List

import kognic.io.client as IOC
import kognic.io.model as IAM


def run(client: IOC.KognicIOClient) -> List[IAM.SensorCalibrationEntry]:
    print("Listing Calibration...")

    calibrations = client.calibration.get_calibrations()
    print(calibrations)

    return calibrations


if __name__ == "__main__":
    client = IOC.KognicIOClient()
    run(client)
