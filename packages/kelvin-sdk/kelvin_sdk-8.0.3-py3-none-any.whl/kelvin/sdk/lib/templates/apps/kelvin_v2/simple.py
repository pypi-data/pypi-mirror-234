import asyncio

from kelvin.app.client import KelvinApp
from kelvin.message import Number
from kelvin.message.krn import KRNAssetDataStream


async def main() -> None:
    # Creatiing instance of Kelvin App Client
    kelvin_app = KelvinApp()

    # Connect the App Client
    await kelvin_app.connect()

    # Custom Loop
    while True:
        # Publish Data (Number) -> 50.0
        await kelvin_app.publish_message(
            Number(resource=KRNAssetDataStream("<asset_name>", "<output_name>"), payload=50.0)
        )

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
