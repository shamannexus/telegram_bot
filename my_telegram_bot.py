import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes, CallbackContext
)
import datetime
from telegram import BotCommand

TOKEN = '8020783210:AAHiNh4XTnMkYaD2hYvh3Csa10lU6IG2uv8'
MANAGER_USERNAME = "shamannexus"
INSTAGRAM_USERNAME = "pheobyandrachel"
COMMUNITY_URL = "https://t.me/shaman_test_1"

# Лічильник, який буде зберігати який зараз номер фото
current_index = 1

# Dictionary mapping button presses to Google Drive links
video_urls = {
    'video1': 'https://drive.google.com/uc?export=download&id=1_8d2LsqDRC1RwY1hTUj6ZXHEiNpuQFyW',
    'video2': 'https://drive.google.com/uc?export=download&id=1rN6eNzmZ0jZ19fUa2Z3RvTYM0dDOCB1V',
    'video3': 'https://drive.google.com/uc?export=download&id=1WoBoKeoLp1nRqZqT-kR9SWRTCKM5JuXY',
    'video4': 'https://drive.google.com/uc?export=download&id=1vciy0FvHqwvxHDmhglP0OlTOm3K9E8Hx',
}

photos = {
    "intro": "https://drive.google.com/uc?export=download&id=1hXkBmcdOFGYTjKr3h1YbzPHlNLPL29_F",
    "intro2": "https://drive.google.com/uc?export=download&id=1Y8cWLZYiMD5Pz0oTCQEYKzuNXpRFyB_N",
    "reminder": "https://drive.google.com/uc?export=download&id=18QsNM6XMsDkle64kjBMOGh3frqVzgg1P",
    # можеш додати інші фото сюди
}

content = {
    1: {"photo": "https://drive.google.com/uc?export=download&id=1Y8cWLZYiMD5Pz0oTCQEYKzuNXpRFyB_N", "caption": "🐶 Фібі: Привіт! Я твій новий тренер. А Рейчел каже: не спізнюйся на заняття!"},
    2: {"photo": "https://drive.google.com/uc?export=download&id=1hXkBmcdOFGYTjKr3h1YbzPHlNLPL29_F", "caption": "🐾 Рейчел: Сьогодні ми тренуємо хвостик. Фібі вже розігріває лапки!"},
    3: {"photo": "https://drive.google.com/uc?export=download&id=1ZfbBJId70Cm6t54UQiF_3-3LDRsN7ANq", "caption": "🐕 Фібі: Якщо хочеш печенько — то спочатку команда 'сидіти'! Рейчел перевірить 😉"},
    4: {"photo": "https://drive.google.com/uc?export=download&id=17PuscSxNykjhzRf4sclYqUZlzddgXEIA", "caption": "🐶 Рейчел: Гав-гав! Час рухатись. Фібі вже крутанула коло!"},
    5: {"photo": "https://drive.google.com/uc?export=download&id=1OsUI7VEpUpkX6GzMf69I04kgGNL-EAhe", "caption": "🐾 Фібі: Якщо втомився — лягай. Рейчел: але тільки після вправ!"},
    6: {"photo": "https://drive.google.com/uc?export=download&id=11kJoZnkZcc5aOhe0i2f9M52J8WmJKWfE", "caption": "🐕 Рейчел: Ти вже майже пес! Фібі підморгує: залишилось ще трошки."},
    7: {"photo": "https://drive.google.com/uc?export=download&id=1t5SnmGc3baRgKYze6oE_zkEaFZofP3RF", "caption": "🐶 Фібі: Бери приклад з мене. Рейчел: але не гавкай на листоношу 😅"},
    8: {"photo": "https://drive.google.com/uc?export=download&id=1OmTwGkAHXP2vvd2rhSI28oIuZMB2Uuag", "caption": "🐾 Рейчел: Сьогодні танці лапами! Фібі вже крутиться як балерина."},
    9: {"photo": "https://drive.google.com/uc?export=download&id=1VEyIdF0Wns5ERtRs0jWC_CJRCEBgUKYg", "caption": "🐕 Фібі: Не забудь посмішку. Рейчел: і хвостиком повиляй!"},
    10: {"photo": "https://drive.google.com/uc?export=download&id=1-gtLcXRKIUL_pAaYsC8uUlQDW3YRpYaa", "caption": "🐶 Рейчел: Ти молодець! Фібі: а я вже облизала миску після тренування."},
    11: {"photo": "https://drive.google.com/uc?export=download&id=1cEN1Q6KeGh2vBWBZ-GgsErd1-DJm3tvE", "caption": "🐶 Фібі: Я прокинулась! Рейчел каже: пора вставати й тренуватись!"},
    12: {"photo": "https://drive.google.com/uc?export=download&id=1tAJes3BaIC1XKCjkTflICp64Ab-Yse6k", "caption": "🐾 Рейчел: Ходи зі мною на прогулянку. Фібі вже знайшла нову паличку."},
    13: {"photo": "https://drive.google.com/uc?export=download&id=1iYz-G6u8XqT0ZmoV_60NmeWQ1tOalFlE", "caption": "🐕 Фібі: Якщо впав — вставай. Рейчел: і не забудь потрусити вушками!"},
    14: {"photo": "https://drive.google.com/uc?export=download&id=1MGQw6l9ZorgdjnkQUEpPn00Py4vZtz0o", "caption": "🐶 Рейчел: Мрії збуваються. Фібі: особливо якщо там є кісточки."},
    15: {"photo": "https://drive.google.com/uc?export=download&id=12zHnU4v-IkR7hrW4HozgG8sHoe3F2_K8", "caption": "🐾 Фібі: Я сьогодні чемна. Рейчел: і ти теж спробуй!"},
    16: {"photo": "https://drive.google.com/uc?export=download&id=1bsQAeWcGUM5wGLTJJIX6FwKih03qrfsX", "caption": "🐕 Рейчел: Бігти швидко — це кайф! Фібі: головне не впасти в калюжу."},
    17: {"photo": "https://drive.google.com/uc?export=download&id=1JZQqHpUG6VxYtNBbhIXtC1996AIdVFq6", "caption": "🐶 Фібі: Я люблю сонце. Рейчел: але більше люблю твої смаколики!"},
    18: {"photo": "https://drive.google.com/uc?export=download&id=1GX2BPn4R6oOdlPzPaiwJz9XqXvZQbylj", "caption": "🐾 Рейчел: Вір у себе! Фібі вже вірить у тебе."},
    19: {"photo": "https://drive.google.com/uc?export=download&id=1m7h1GJG8J3FNtjUbZaImAfXKQjBvrBOX", "caption": "🐕 Фібі: Нюхай життя! Рейчел: і завжди wag-wag хвостиком."},
    20: {"photo": "https://drive.google.com/uc?export=download&id=1yP8XhlgcL2SZTvM_UfwKKJW40chO3Ulj", "caption": "🎉 Фібі: Молодець! Рейчел: Ти майже пес ❤️"},
    21: {"photo": "https://drive.google.com/uc?export=download&id=1Gu1igxXkDvEtjTPFim9GBxnsJ5rWowRw", "caption": "🐶 Фібі: Вухо до вуха — так виглядає справжня посмішка! Рейчел підтверджує."},
    22: {"photo": "https://drive.google.com/uc?export=download&id=1Ki8LaNuYUyYl3m845ydahUu91JuNhpzS", "caption": "🐾 Рейчел: Якщо важко — обійми. Фібі: я вже готова!"},
    23: {"photo": "https://drive.google.com/uc?export=download&id=1saMtofNvwXSLL6J8LuBYiNa6XCn_of51", "caption": "🐕 Фібі: Лай — це мова любові. Рейчел: і ще трішки шуму."},
    24: {"photo": "https://drive.google.com/uc?export=download&id=1kHgjMvsP_WgB2WTwzQ3sDdJri-ZberQC", "caption": "🐶 Рейчел: Відпочинок — теж тренування. Фібі: особливо на подушці."},
    25: {"photo": "https://drive.google.com/uc?export=download&id=1GtIxkzOveoEozmVwKryhsA-eEnjXY3t4", "caption": "🐾 Фібі: Не здавайся! Рейчел: бо ми завжди поруч."},
    26: {"photo": "https://drive.google.com/uc?export=download&id=1W9FzHi_qEWm5zY-X6fWcvqNxu4a9TJz8", "caption": "🐕 Рейчел: Я люблю бігати. Фібі: але ще більше люблю обійми!"},
    27: {"photo": "https://drive.google.com/uc?export=download&id=1wgwOJygShBhZoCxDnvIroMId1JC94Af8", "caption": "🐶 Фібі: Хочеш кістку? Рейчел: виконай команду!"},
    28: {"photo": "https://drive.google.com/uc?export=download&id=1WC3CKcYPNEHTmt1t_Hz_8N1atTHrQMxa", "caption": "🐾 Рейчел: Завжди мрій. Фібі: і буде більше смаколиків."},
    29: {"photo": "https://drive.google.com/uc?export=download&id=138bpcwpCt-Qyqbg_xVnGZi0aIkqqqVZS", "caption": "🐕 Фібі: Якщо день поганий — покрути хвостиком. Рейчел: одразу стане краще!"},
    30: {"photo": "https://drive.google.com/uc?export=download&id=1CgBqW8vDRR2YrawdgZi4b_RsAo2Qlv2b", "caption": "🐶 Рейчел: Ти герой! Фібі: лапами аплодую."},
    31: {"photo": "https://drive.google.com/uc?export=download&id=1l93T7G5my7eMgcHUX1PsNqu8xiBOHDNF", "caption": "🐶 Фібі: Навіть песики роблять помилки. Рейчел: головне — не кусай тапки."},
    32: {"photo": "https://drive.google.com/uc?export=download&id=15SrMhDMUcvQqciRtqxy99u5FevDfm5Hy", "caption": "🐾 Рейчел: Ти можеш усе! Фібі: я вже вірю в тебе."},
    33: {"photo": "https://drive.google.com/uc?export=download&id=1ft3Tv6rvPsXCHo5QPMVmGw1DWS5o8cqi", "caption": "🐕 Фібі: Іноді потрібно просто поспати. Рейчел: на моєму ліжку 😅"},
    34: {"photo": "https://drive.google.com/uc?export=download&id=1UzmaaFxFseR0El_Xq2GcnYlO3z3hF2NO", "caption": "🐶 Рейчел: Навчання робить досконалим. Фібі: особливо коли є смаколики!"},
    35: {"photo": "https://drive.google.com/uc?export=download&id=1PoDtzyUXRf5qqRYPNeZ3XZjE-WaSzySu", "caption": "🐾 Фібі: Вір у дива. Рейчел: бо кістки знаходяться навіть у піску."},
    36: {"photo": "https://drive.google.com/uc?export=download&id=1ft1aG8LZsICEPc7fa6Wc_1GKaqMI3PfH", "caption": "🐕 Рейчел: Тренування лапок — наше все! Фібі вже присіла."},
    37: {"photo": "https://drive.google.com/uc?export=download&id=1RIejioZOSu-4KzUkA0wJeJqsu00kosn3", "caption": "🐶 Фібі: Ти крута! Рейчел: а я ще крутіша 🐾"},
    38: {"photo": "https://drive.google.com/uc?export=download&id=18QsNM6XMsDkle64kjBMOGh3frqVzgg1P", "caption": "🐾 Рейчел: Любов — це коли гавкаєш удвох. Фібі згодна."},
    39: {"photo": "https://drive.google.com/uc?export=download&id=15FbA_8U3g7qS8u7DHxVM9IK6t6FZksSf", "caption": "🐕 Фібі: Дивись вперед. Рейчел: і нюхай свіже повітря."},
    40: {"photo": "https://drive.google.com/uc?export=download&id=1J2TkPC8-qXMcLq2wGmS0M4tuPsz1o0ai", "caption": "🐶 Рейчел: Позитив — це як грайливий гавкіт. Фібі додає — гав-гав!"},
    41: {"photo": "https://drive.google.com/uc?export=download&id=1lVkOmegwoSziEx_kBGq7-3NvzvjzfZwf", "caption": "🐶 Фібі: Потрібно вчитись кожен день. Рейчел: і ще трішки бігати!"},
    42: {"photo": "https://drive.google.com/uc?export=download&id=16JOrZGpZo_r-AyWCZtTDXd78KngOXW0O", "caption": "🐾 Рейчел: Слухай серце. Фібі: воно гавкає правильно."},
    43: {"photo": "https://drive.google.com/uc?export=download&id=16JOrZGpZo_r-AyWCZtTDXd78KngOXW0O", "caption": "🐕 Фібі: Якщо дощ — все одно гуляй. Рейчел: я візьму плащик 🐾"},
    44: {"photo": "https://drive.google.com/uc?export=download&id=1xlJ6c0RhxL3Qh0i756PPFQH2kWYvnjV0", "caption": "🐶 Рейчел: Друзі — це скарб. Фібі: і вони гавкають разом."},
    45: {"photo": "https://drive.google.com/uc?export=download&id=1BWd3M4JPU13NueU0FRcO-LxOra0iaEPi", "caption": "🐾 Фібі: Можна трошки полінитись. Рейчел: але потім знову бігай!"},
    46: {"photo": "https://drive.google.com/uc?export=download&id=1EerHQSQ4yH1aVEEuYyp7nIj3Auvj_EMP", "caption": "🐕 Рейчел: Сон — найкращий відпочинок. Фібі: особливо на твоїй подушці."},
    47: {"photo": "https://drive.google.com/uc?export=download&id=17x1h8pVnItUQTsSaXsk8khINNe2dsWi3", "caption": "🐶 Фібі: Ми горді за тебе! Рейчел: хвіст вгору!"},
    48: {"photo": "https://drive.google.com/uc?export=download&id=1iEKbOsJo_6IqGfByHTfEsZx_wXQy53nx", "caption": "🐾 Рейчел: Ти вже чемпіон. Фібі: гав-гав у твою честь!"},
    49: {"photo": "https://drive.google.com/uc?export=download&id=1OeDgeHYsUgrt2KssDC6orx9LTrDOnM7U" , "caption": "🐕 Фібі: Ти найкращий друг песиків. Рейчел: лапи аплодисментами!"},
    50: {"photo": "https://drive.google.com/uc?export=download&id=1BMw9XlDVfHpXu_sZmNlbn8cwrPdFu78-", "caption": "🎉 Фібі: Ура, фініш! Рейчел: тепер ти справжній член нашої зграї ❤️"},
}

def main_menu_markup() -> InlineKeyboardMarkup:
    video_keyboard = [
        [
            InlineKeyboardButton("🎬 Відео 1", callback_data='video1'),
            InlineKeyboardButton("🎬 Відео 2", callback_data='video2'),
        ],
        [
            InlineKeyboardButton("🎬 Відео 3", callback_data='video3'),
            InlineKeyboardButton("🎬 Відео 4", callback_data='video4'),
        ],
    ]
    community_keyboard = [
        [InlineKeyboardButton("📢 Приєднатися до спільноти", url=COMMUNITY_URL)]
    ]
    return InlineKeyboardMarkup(video_keyboard + community_keyboard)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await send_advert_now(update.message.chat_id, context)

    await update.message.reply_text(
        "Оберіть відео або приєднайтеся до спільноти:",
        reply_markup=main_menu_markup()
    )

    await send_intro_info_with_instagram_subscription(update.message.chat_id, context)
    await send_info_with_courses(update.message.chat_id, context)

    # розсилка щогодини (3600 сек) з затримкою 5 сек після старту
    context.application.job_queue.run_repeating(send_advert_job, interval=86400, first=900, chat_id=update.message.chat_id)

    context.application.job_queue.run_repeating(send_daily_content, interval=60*60, first=5, chat_id=update.message.chat_id)



async def send_intro_info_with_instagram_subscription(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("Підпишися на інсту", url=f"https://www.instagram.com/{INSTAGRAM_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=photos["intro"],
        caption="""🔥Привіт! Ми ФІбі і Рейчел і ми навчимо вас як бути собаками!!!
Трохи про нас:
        
ФІбі – з польської родини 🏡, справжня панянка, яка любить прогулюватися в парку і ганяти м’ячики.
        
Рейчел – справжня героїня! 🐶💛 Волонтери привезли її з України, вона біженка, бо втекла від війни. Тепер вона вчиться жити щасливо і ділиться своїм оптимізмом зі всіма.
            """,
        reply_markup=reply_markup
    )

async def send_info_with_courses(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("Купити курс!!!", url=f"https://t.me/{MANAGER_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=photos["intro2"],
        caption="""На наших курсах ви дізнаєтесь:

Як правильно ганяти хвіст 🐕

Мяукати на пошту 📨 … ой, ні, це для котів 😅

Ловити м’ячики будь-якої форми 🎾

Спати на дивані як професіонал 🛋️

І звісно — як отримати максимум ласки від людей ❤️

Приєднуйтесь і станьте супер-собаками разом з нами! 🐶✨""",
        reply_markup=reply_markup
    )

# Відправка картинки одразу
async def send_advert_now(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("💬 Написати менеджеру", url=f"https://t.me/{MANAGER_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=photos["reminder"],
        caption="🔥Привіт! Нагадуємо, що ти ще не записався на навчання! Запишіться вже зараз!",
        reply_markup=reply_markup
    )

# Відправка картинки для JobQueue
async def send_advert_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    await send_advert_now(chat_id, context)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in video_urls:
        video_url = video_urls[query.data]
        video_path = f"{query.data}.mp4"

        # Завантаження відео
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(video_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            # Відправка відео у Telegram
            with open(video_path, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=query.message.chat.id,
                    video=video_file,
                    caption=f"Ваше відео: {query.data}"
                )

            os.remove(video_path)  # чистимо після відправки
        else:
            await query.edit_message_text(text="❌ Помилка завантаження відео.")
    elif query.data == "menu":
        await query.edit_message_text(
            text="Оберіть відео або приєднайтеся до спільноти:",
            reply_markup=main_menu_markup()
        )
    else:
        await query.edit_message_text(text="Невідома кнопка.")



async def send_daily_content(context: CallbackContext) -> None:
    global current_index

    chat_id = context.job.chat_id
    now = datetime.datetime.now().time()

    # Дозволені години (8:00 - 22:00)
    start_time = datetime.time(8, 0)
    end_time = datetime.time(23, 0)

    if start_time <= now <= end_time:
        # Беремо фото по ключу
        item = content[current_index]

        # keyboard = [
        #     [InlineKeyboardButton("💬 Написати менеджеру", url="https://t.me/shamannexus")]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=item["photo"],
            caption=item["caption"],
            # reply_markup=reply_markup
        )

        # Наступна картинка (якщо більше 20 → почати з 1)
        current_index += 1
        if current_index > len(content):
            current_index = 1

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
