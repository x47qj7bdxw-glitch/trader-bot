import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Получаем токен из переменной окружения (Render)
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise Exception("API_TOKEN не найден! Добавь переменную окружения на Render или локально.")

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot_log.txt",
    filemode="a"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Исходная ветка (откуда брать сообщения)
source_chat_id = -1003535658160
source_thread_id = 412

# Чат назначения (куда пересылать сообщения)
destination_chat_id = -1003696389874

# Словарь трейдеров → их ветки в чате назначения
traders_threads = {
    7575282612: 8,
    7276227554: 13,
    8521137714: 5,
    1341379811: 18,
    8126450181: 16,
    343595815: 2,
    5593264601: 15,
    1604725555: 17
}

@dp.message_handler()
async def forward_from_general(message: types.Message):
    try:
        # Проверяем, что сообщение из нужной общей ветки
        if message.chat.id == source_chat_id and message.message_thread_id == source_thread_id:
            sender_id = message.from_user.id
            if sender_id in traders_threads:
                thread_id = traders_threads[sender_id]

                # Форвардим сообщение в ветку трейдера
                await bot.forward_message(
                    chat_id=destination_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    message_thread_id=thread_id
                )

                # Логируем успех
                logging.info(f"Forwarded message from {sender_id} to thread {thread_id}")
                print(f"Forwarded message from {sender_id} to thread {thread_id}")

    except Exception as e:
        logging.error(f"Error forwarding message: {e}")
        print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("Bot started... Listening for messages")
    executor.start_polling(dp, skip_updates=True)
