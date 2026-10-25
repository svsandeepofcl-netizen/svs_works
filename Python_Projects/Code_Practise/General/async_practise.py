import asyncio


async def task(name):
    print(f"Recieved Task {name}")
    await asyncio.sleep(2)
    print(f"Completed Task {name}")


async def main():
    await asyncio.gather(

        task("A"),
        task("B")
    )

asyncio.run(main())