import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, CallbackContext
)

TOKEN = '8020783210:AAHEtJHTC0Hen5ZbQnW7YYQulRDubcoPVBc'

# Dictionary mapping button presses to Google Drive links
video_urls = {
    'video1': 'https://drive.google.com/uc?export=download&id=1_8d2LsqDRC1RwY1hTUj6ZXHEiNpuQFyW',
    'video2': 'https://drive.google.com/uc?export=download&id=1rN6eNzmZ0jZ19fUa2Z3RvTYM0dDOCB1V',
    'video3': 'https://drive.google.com/uc?export=download&id=1WoBoKeoLp1nRqZqT-kR9SWRTCKM5JuXY',
    'video4': 'https://drive.google.com/uc?export=download&id=1vciy0FvHqwvxHDmhglP0OlTOm3K9E8Hx',
}

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Отримати Відео 1", callback_data='video1')],
        [InlineKeyboardButton("Отримати Відео 2", callback_data='video2')],
        [InlineKeyboardButton("Отримати Відео 3", callback_data='video3')],
        [InlineKeyboardButton("Отримати Відео 4", callback_data='video4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Оберіть відео:", reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in video_urls:
        video_url = video_urls[query.data]

        # Download the video file
        video_path = f"{query.data}.mp4"
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(video_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            # Send video to Telegram
            with open(video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=query.message.chat_id, video=video_file,
                                             caption=f"Ваше відео: {query.data}")

            # Remove the downloaded file to save space
            os.remove(video_path)
        else:
            await query.edit_message_text(text="Помилка завантаження відео.")
    else:
        await query.edit_message_text(text="Невідома кнопка.")


# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()