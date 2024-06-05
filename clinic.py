from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7065204961:AAE52Jnj5pj-LTQxcBYQqMyiruV3Dl9JiCw'

# Ключ от API UNSPLASH 
UNSPLASH_ACCESS_KEY = '0zHx_eFJCR9o3CXv8x3vN_QwjaZkWj5egtmbJ1TDVbc'

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Услуги", callback_data='directory')],
        [InlineKeyboardButton("Наш сайт", url='https://sevakargashin.tilda.ws/')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'nachalo':
        keyboard = [
            [InlineKeyboardButton("Услуги", callback_data='directory')],
            [InlineKeyboardButton("Наш сайт", url='https://sevakargashin.tilda.ws/')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите раздел:", reply_markup=reply_markup)

    elif data == 'directory':
        keyboard = [
            [InlineKeyboardButton("Кастрация", callback_data='castr')],
            [InlineKeyboardButton("Вакцинация", callback_data='vaks')],
            [InlineKeyboardButton("Терапия", callback_data='terap')],
            [InlineKeyboardButton("Назад", callback_data='nachalo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите раздел:", reply_markup=reply_markup)

    elif data == 'castr':
        keyboard = [
            [InlineKeyboardButton("Абкаликов Н.А.", callback_data='abkalik')],
            [InlineKeyboardButton("Зубин К.В.", callback_data='zubin')],
            [InlineKeyboardButton("Назад", callback_data='directory')],
            [InlineKeyboardButton("Главная страница", callback_data='nachalo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите мастера по кастрации:", reply_markup=reply_markup)

    elif data == 'vaks':
        keyboard = [
            [InlineKeyboardButton("Каргашин В.В.", callback_data='kargashin')],
            [InlineKeyboardButton("Юхнин В.А.", callback_data='yuha')],
            [InlineKeyboardButton("Назад", callback_data='directory')],
            [InlineKeyboardButton("Главная страница", callback_data='nachalo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите мастера по прививкам:", reply_markup=reply_markup)

    elif data == 'terap':
        keyboard = [
            [InlineKeyboardButton("Антропов В.А.", callback_data='antropov')],
            [InlineKeyboardButton("Сальников Р.В.", callback_data='salnikov')],
            [InlineKeyboardButton("Назад", callback_data='directory')],
            [InlineKeyboardButton("Главная страница", callback_data='nachalo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите терапевта:", reply_markup=reply_markup)

    elif data in ['abkalik', 'zubin', 'kargashin', 'yuha', 'antropov', 'salnikov']:
        doctor_info = {
            'abkalik': "Абкаликов Н.А.\nТелефон: +7(951)963-58-79\n[Telegram](https://t.me/makoley_kalk1n)",
            'zubin': "Зубин К.В.\nТелефон: +7(962)544-39-60\n[Telegram](https://t.me/KiriIlIl)",
            'kargashin': "Каргашин В.В.\nТелефон: +7(951)203-39-60\n[Telegram](https://t.me/lamuzikasw)",
            'yuha': "Юхнин В.А.\nТелефон: +7(933)568-98-98\n[Telegram](https://t.me/YushaYubo4kaisPlusHa)",
            'antropov': "Антропов В.А.\nТелефон: +7(951)204-55-99\n[Telegram](https://t.me/blyadovladd)",
            'salnikov': "Сальников Р.В.\nТелефон: +7(951)210-12-99\n[Telegram](https://t.me/RomanSalnikov06)"
        }
        
        back_callback_data = 'castr' if data in ['abkalik', 'zubin'] else 'vaks' if data in ['kargashin', 'yuha'] else 'terap'
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data=back_callback_data)],
            [InlineKeyboardButton("Главная страница", callback_data='nachalo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=doctor_info[data], reply_markup=reply_markup, parse_mode='Markdown')

    elif data == 'start':
        await start(update, context)

async def send_random_image(update: Update, context: CallbackContext) -> None:
    url = f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        await update.message.reply_photo(photo=image_url)
    else:
        await update.message.reply_text("Не удалось получить изображение. Попробуйте еще раз позже.")

async def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_random_image))
    app.add_error_handler(error)
    
    app.run_polling()

if __name__ == '__main__':
    main()
