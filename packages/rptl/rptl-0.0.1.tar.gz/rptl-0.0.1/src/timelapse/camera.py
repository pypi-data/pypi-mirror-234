import logging
import time

from picamera2 import Picamera2
from libcamera import controls


logger = logging.getLogger(__name__)


"""
https://github.com/raspberrypi/picamera2/blob/main/examples/capture_timelapse.py
"""

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        logger.debug(f"Camera: {self.picam2}")
        self.config = self.picam2.create_still_configuration()

        # self.config.lens_position = 10

        self.picam2.configure(self.config)
        logger.debug(f"Config: {self.config}")

        # Give time for Aec and Awb to settle, before disabling them
        logger.debug("Waiting for Aec and Awb to settle.")
        time.sleep(2)
        #logger.debug("Disabling Aec and Awb.")
        self.picam2.set_controls({"AeEnable": True, "AwbEnable": False, "FrameRate": 1.0})
        # And wait for those settings to take effect
        logger.debug("Waiting for Aec and Awb to settle.")
        time.sleep(2)

        logger.debug("Setting lens position.")
        self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 5.0})

        # logger.debug("Setting exposure.")
        # i think you can only get the metadata after you've started the camera
        #metadata = self.picam2.capture_metadata()
        #exposure_normal = metadata["ExposureTime"]
        #gain = metadata["AnalogueGain"] * metadata["DigitalGain"]
        #breakpoint()
        # exposure_normal = 1500
        # self.picam2.set_controls({"ExposureTime": exposure_normal})

        self.start()

    def set_hdr(self, enable=True):
        wdr_value = "1" if enable else "0"
        # f"v4l2-ctl --set-ctrl wide_dynamic_range={wdr_value} -d /dev/v4l-subdev0"
        pass

    def start(self):
        logger.debug("Starting camera.")
        self.picam2.start()


    def capture_still(self, filename):
        logger.info(f"Capturing still to {filename}")
        r = self.picam2.capture_request()
        r.save("main", filename)
        r.release()
        logger.info(f"Captured still to {filename}")

    def stop(self):
        logger.debug("Stopping camera.")
        self.picam2.stop()

