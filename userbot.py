import os
import logging
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = "userbot"

# ===== Чаты =====
source_chat_id = -1003535658160
source_thread_id = 412
destination_chat_id = -1003696389874

# ===== Словарь трейдеров =====
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Client(session_name, api_id=api_id, api_hash=api_hash)

# ===== Ловим сообщения строго из ветки форума =====
@app.on_message(filters.chat(source_chat_id) & filters.forum(source_thread_id))
async def forward_message(client, message):
    sender_id = message.from_user.id if message.from_user else None
    if not sender_id or sender_id not in traders_threads:
        return

    thread_id = traders_threads[sender_id]
    caption_prefix = f"[Трейдер {sender_id}]: "

    try:
        if message.text:
            await client.send_message(destination_chat_id, caption_prefix + message.text, message_thread_id=thread_id)
        elif message.photo:
            await client.send_photo(destination_chat_id, message.photo.file_id, caption=caption_prefix + (message.caption or ""), message_thread_id=thread_id)
        elif message.video:
            await client.send_video(destination_chat_id, message.video.file_id, caption=caption_prefix + (message.caption or ""), message_thread_id=thread_id)
        elif message.document:
            await client.send_document(destination_chat_id, message.document.file_id, caption=caption_prefix + (message.caption or ""), message_thread_id=thread_id)
        elif message.sticker:
            await client.send_sticker(destination_chat_id, message.sticker.file_id, message_thread_id=thread_id)

        logging.info(f"Forwarded message from {sender_id} to thread {thread_id}")

    except Exception as e:
        logging.error(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("Userbot started, listening for messages...")
    app.run()
