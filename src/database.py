from tortoise import Tortoise, run_async


async def connectToDatabase():
    await Tortoise.init(
        db_url='postgres://postgres:8s8wxa@localhost:5433/user_service_db',
        modules={'models': ['models']}
    )


async def main():
    await connectToDatabase()
    await Tortoise.generate_schemas()


if __name__ == 'main':
    run_async(main())
