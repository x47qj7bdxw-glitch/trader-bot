import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor  # для aiogram 2.x

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

# Исходный чат и ветка (только эта ветка читаем)
source_chat_id = -1003535658160
source_thread_id = 412  # конкретная ветка

# Чат назначения
destination_chat_id = -1003696389874

# Словарь трейдеров: ключ = ID трейдера, значение = ветка в destination
traders_threads = {
    7575282612: 8,
    7276227554: 13,
    8521137714: 5,
    1341379811: 18,
    8126450181: 16,
    343595815: 2,
    5593264601: 15,
    1604725555: 17,
    470443361: 9
}

@dp.message_handler()
async def forward_from_specific_thread(message: types.Message):
    try:
        # Только сообщения из нужной ветки исходного чата
        if message.chat.id == source_chat_id and message.message_thread_id == source_thread_id:
            sender_id = message.from_user.id
            if sender_id in traders_threads:
                thread_id = traders_threads[sender_id]  # ветка в destination
                await bot.copy_message(
                    chat_id=destination_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    message_thread_id=thread_id
                )
                print(f"Copied message from {sender_id} to thread {thread_id}")
                logging.info(f"Copied message from {sender_id} to thread {thread_id}")
    except Exception as e:
        print(f"Error copying message: {e}")
        logging.error(f"Error copying message: {e}")

if __name__ == "__main__":
    print("Bot started... Listening for messages")
    executor.start_polling(dp, skip_updates=True)
