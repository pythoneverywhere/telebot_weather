from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
from services.queue_manager import QueueManager
from db.models import add_user


class HandlerManager:
    _instance = None

    def __new__(cls, bot: Bot, queue_manager: QueueManager):
        if cls._instance is None:
            cls._instance = super(HandlerManager, cls).__new__(cls)
            cls._instance.bot = bot
            cls._instance.queue_manager = queue_manager
        return cls._instance

    def __init__(self, bot: Bot, queue_manager: QueueManager):
        self.bot = bot
        self.queue_manager = queue_manager

    async def start_command(self, message: Message):
        user_id = message.from_user.id
        try:
            add_user(user_id)
            added_to_queue = await self.queue_manager.add_to_queue(user_id)
            position = await self.queue_manager.number_queue(user_id)

            if added_to_queue:
                await message.reply(f"я добавил вас в очередь, ваш номер: {position}")
                await self.queue_manager.process_queue(self.bot)
            else:
                await message.reply(f"вы уже в очереди, ваш номер: {position}")
        except Exception as e:
            await message.reply(f'ошибка: {e}')

    async def info_command(self, message: Message):
        try:
            await self.queue_manager.info_queue(message)
        except Exception as e:
            await message.reply(f"ошибка: {e}")

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.start_command, Command("start"))
        dp.message.register(self.info_command, Command("info"))
