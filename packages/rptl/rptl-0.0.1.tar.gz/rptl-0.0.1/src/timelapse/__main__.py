import asyncio
import logging

from timelapse.daemon import Daemon


logger = logging.getLogger(__name__)


async def _main():
    daemon = Daemon()
    daemon.start()

    tasks = [
        asyncio.create_task(daemon.run_timelapse()),
        asyncio.create_task(daemon.run_timestamp_images()),
        asyncio.create_task(daemon.run_sort_colour_profile()),
        asyncio.create_task(daemon.zmq_server()),
    ]

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

def main():
    logging.basicConfig(
        # level=opts["--log-level"],
        level="INFO",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    asyncio.run(_main())

if __name__ == "__main__":
    main()