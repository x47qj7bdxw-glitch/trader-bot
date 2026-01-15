import os
import logging
from pyrogram import Client, filters
from dotenv import load_dotenv

# ===== Загружаем переменные окружения =====
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = "userbot"

# ===== Чаты =====
source_chat_id = -1003535658160  # исходный чат
source_thread_id = 412           # ветка форума
destination_chat_id = -1003696389874  # чат назначения

# ===== Словарь трейдеров =====
# ключ = ID трейдера, значение = ветка назначения
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

# ===== Логи =====
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Client(session_name, api_id=api_id, api_hash=api_hash)

# ===== Ловим все сообщения из исходного чата =====
@app.on_message(filters.chat(source_chat_id))
async def forward_message(client, message):
    try:
        # ===== Проверяем ветку форума вручную =====
        if getattr(message, "message_thread_id", None) != source_thread_id:
            return  # не наша ветка

        sender_id = message.from_user.id if message.from_user else None
        if not sender_id or sender_id not in traders_threads:
            return

        thread_id = traders_threads[sender_id]
        caption_prefix = f"[Трейдер {sender_id}]: "

        # ===== Текст =====
        if message.text:
            await client.send_message(
                chat_id=destination_chat_id,
                text=caption_prefix + message.text,
                message_thread_id=thread_id
            )

        # ===== Фото =====
        elif message.photo:
            await client.send_photo(
                chat_id=destination_chat_id,
                photo=message.photo.file_id,
                caption=caption_prefix + (message.caption or ""),
                message_thread_id=thread_id
            )

        # ===== Видео =====
        elif message.video:
            await client.send_video(
                chat_id=destination_chat_id,
                video=message.video.file_id,
                caption=caption_prefix + (message.caption or ""),
                message_thread_id=thread_id
            )

        # ===== Документы =====
        elif message.document:
            await client.send_document(
                chat_id=destination_chat_id,
                document=message.document.file_id,
                caption=caption_prefix + (message.caption or ""),
                message_thread_id=thread_id
            )

        # ===== Стикеры =====
        elif message.sticker:
            await client.send_sticker(
                chat_id=destination_chat_id,
                sticker=message.sticker.file_id,
                message_thread_id=thread_id
            )

        logging.info(f"Forwarded message from {sender_id} to thread {thread_id}")

    except Exception as e:
        logging.error(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("Userbot started, listening for messages...")
    app.run()
    
