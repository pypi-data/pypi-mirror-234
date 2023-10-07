from kognic.io.model.calibration.camera.common import BaseCameraCalibration, DistortionCoefficients
from kognic.io.model.calibration.common import CalibrationType


class FisheyeCalibration(BaseCameraCalibration):
    calibration_type = CalibrationType.FISHEYE
    distortion_coefficients: DistortionCoefficients
    xi: float
