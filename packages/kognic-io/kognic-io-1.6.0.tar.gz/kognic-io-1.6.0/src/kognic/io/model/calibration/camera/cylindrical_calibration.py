from kognic.io.model.calibration.camera.common import BaseCameraCalibration
from kognic.io.model.calibration.common import CalibrationType


class CylindricalCalibration(BaseCameraCalibration):
    calibration_type = CalibrationType.CYLINDRICAL
