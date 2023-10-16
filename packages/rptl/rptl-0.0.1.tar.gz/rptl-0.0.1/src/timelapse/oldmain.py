import logging
import time
from datetime import datetime
from pathlib import Path

from timelapse.camera import Camera


logger = logging.getLogger(__name__)


def main():
    running = True
    camera = Camera()
    camera.start()

    timelapse_interval = 300
    # 6 hours
    # timelapse_duration = 6 * 60 * 60

    # log the datetime timestamp when we last took a stil
    last_still_timestamp = None

    while running:
        logger.debug(f"Running: {running}")
        try:
            if last_still_timestamp != None and (datetime.now() - last_still_timestamp).seconds < timelapse_interval:
                # calculate how long to sleep for based on the timelapse_interval
                time_to_sleep = timelapse_interval - (datetime.now() - last_still_timestamp).seconds
                logger.debug(f"Sleeping for {time_to_sleep} seconds.")
                time.sleep(time_to_sleep)
                continue

            last_still_timestamp = datetime.now()

            dir_name = datetime.now().strftime("%Y%m%d")

            # create the directory if it doesn't exist
            Path(f"images/{dir_name}").mkdir(parents=True, exist_ok=True)

            filename = f"images/{dir_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            camera.capture_still(filename)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt, exiting.")
            running = False

    camera.stop()


if __name__ == "__main__":
    logging.basicConfig(
        # level=opts["--log-level"],
        level="DEBUG",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    main()
