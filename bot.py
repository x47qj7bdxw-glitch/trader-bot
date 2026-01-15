import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor  # работает с aiogram 2.x

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise Exception("API_TOKEN не найден! Добавь переменную окружения на Railway")

# Логи
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot_log.txt",
    filemode="a"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Исходный чат (откуда читать сообщения)
source_chat_id = -1003535658160

# Чат назначения (куда форвардить)
destination_chat_id = -1003696389874

# Словарь трейдеров: ключ = Telegram ID, значение = номер ветки (только для справки)
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
        # Проверяем, что сообщение из нужного чата
        if message.chat.id == source_chat_id:
            sender_id = message.from_user.id
            if sender_id in traders_threads:
                # Форвардим сообщение в destination_chat
                await bot.forward_message(
                    chat_id=destination_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
                print(f"Forwarded message from {sender_id}")
                logging.info(f"Forwarded message from {sender_id}")
    except Exception as e:
        print(f"Error forwarding message: {e}")
        logging.error(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("Bot started... Listening for messages")
    executor.start_polling(dp, skip_updates=True)
