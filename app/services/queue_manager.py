import asyncio
from services.weather_service import WeatherService

weather_service = WeatherService()

class QueueManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.queue_list = []

    async def add_to_queue(self, user_id):
        if user_id not in self.queue_list:
            await self.queue.put(user_id)
            self.queue_list.append(user_id)
            return True
        return False

    async def process_queue(self, bot):
        while not self.queue.empty():
            user_id = await self.queue.get()

            await asyncio.sleep(10)

            if user_id in self.queue_list:
                self.queue_list.remove(user_id)

            lat, lon = 56.8389, 60.6057
            weather = weather_service.get_weather(lat, lon)

            message = (
                f"погода екб:\n"
                f"градусов: {weather['temp']}°C\n"
                f"ощущается как: {weather['feels_like']}°C\n"
                f"состояние: {weather['condition']}"
            )

            await bot.send_message(user_id, message)

    async def number_queue(self, user_id):
        try:
            position = self.queue_list.index(user_id) + 1
            return position
        except ValueError:
            return "вас нету в очереди"

    async def info_queue(self, message):
        if self.queue_list:
            queue_info = "\n".join(
                [f"{idx + 1}. id: {user_id}" for idx, user_id in enumerate(self.queue_list)]
            )
            await message.reply(f"очередь:\n{queue_info}")
        else:
            await message.reply("пустая очередь")