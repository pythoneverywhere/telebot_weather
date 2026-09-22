from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import HandlerManager
from services.queue_manager import QueueManager
from db.database import setup_database

API_TOKEN = "token"
# yandex key: key

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    queue_manager = QueueManager()
    handler_manager = HandlerManager(bot, queue_manager)

    setup_database()
    await bot.set_my_commands([
        BotCommand(command="/start", description="start"),
        BotCommand(command="/info", description="info"),
    ])

    handler_manager.register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


#CREATE USER tolik WITH PASSWORD '123';
#CREATE DATABASE datatolik OWNER tolik;
#GRANT ALL PRIVILEGES ON DATABASE datatolik TO tolik;
#peer on md5
