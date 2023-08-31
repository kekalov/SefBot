import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, JobQueue, Dispatcher
import datetime
import random

# Фазы разговора
CHECK_TODAY, DATE = range(2)

# Создайте бота и замените 'YOUR_BOT_TOKEN' на фактический токен вашего бота
bot = telegram.Bot(token='6326442688:AAHcZV3VEzQ9-hbAGGcnA3LF8_nJRsi65wc')

# Функция, которая начинает диалог
def start(update, context):
    user_data = context.user_data
    user_data['date'] = None
    keyboard = [['Да', 'Нет']]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Привет! Cегодня подавали документы?", reply_markup=reply_markup)
    return CHECK_TODAY

# Функция для обработки ответа пользователя о подаче документов сегодня
def check_today(update, context):
    user_data = context.user_data
    user_choice = update.message.text
    if user_choice == 'Да':
        user_data['date'] = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        update.message.reply_text("Отлично! Теперь каждый день жди в 12:00 я буду отправлять тебе кол-во дней и аффирмацию.")
        context.job_queue.run_daily(send_countdown, time=datetime.time(hour=12), days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)
        return ConversationHandler.END
    elif user_choice == 'Нет':
        update.message.reply_text("Введи, пож-та, когда подал документы в формате ГГГГ-ММ-ДД:")
        return DATE

# Функция для остановки работы бота
def stop_bot(update, context):
    user_data = context.user_data
    if user_data['running']:
        update.message.reply_text("Спасибо, что использовали бота! Если вам потребуется еще помощь, просто введите /start.")
        user_data['running'] = False
        context.job_queue.stop()
    else:
        update.message.reply_text("Бот уже остановлен. Если вам потребуется еще помощь, просто введите /start.")

# Функция для обработки введенной даты и установки задачи для отправки сообщения каждый день в 12:00
def set_date(update, context):
    user_data = context.user_data
    try:
        user_date = datetime.datetime.strptime(update.message.text, '%Y-%m-%d')
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if user_date > today:
            user_data['date'] = user_date
            update.message.reply_text("Отлично! Теперь каждый день жди в 12:00 я буду отправлять тебе кол-во дней и аффирмацию")
            context.job_queue.run_daily(send_countdown, time=datetime.time(hour=12), days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)
            return ConversationHandler.END
        else:
            update.message.reply_text("Кстати, ты можемшь ввести дату подачи в будущем.")
            return DATE
    except ValueError:
        update.message.reply_text("Что-то не то с форматом. Пожалуйста, используй формат ГГГГ-ММ-ДД:")
        return DATE

# Функция для отправки сообщения с количеством дней и поговоркой
def send_countdown(context: CallbackContext):
    chat_id = context.job.context
    user_data = context.user_data
    if 'date' in user_data:
        date_diff = (datetime.datetime.now() - user_data['date']).days
        proverb = random.choice(proverbs)  # Здесь вам нужно предоставить список поговорок
        message = f"С даты {user_data['date'].strftime('%Y-%m-%d')} прошло {date_diff} дней.\n{proverb}"
        bot.send_message(chat_id=chat_id, text=message)

# Функция для завершения диалога
def cancel(update, context):
    update.message.reply_text("Чао! Fingers crossed, если буду нужен, то введи /start.")
    return ConversationHandler.END

# Создаем и настраиваем обработчики
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHECK_TODAY: [MessageHandler(Filters.regex(r'^(Да|Нет)$'), check_today)],
        DATE: [MessageHandler(Filters.text & ~Filters.command, set_date)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Создаем обработчик для команды /stop
stop_handler = CommandHandler('stop', stop_bot)



# Создаем список поговорок, которые будут отправляться вместе с количеством дней
proverbs = [
    "SEF в доме - гость в доме.",
    "SEF - капитан своей души.",
    "SEF - не птица, полетишь - устанешь.",
    "Береги SEF семьи, а твоя собственная приумножится.",
    "SEF наверху - дождь на земле.",
    "SEF хорошо, а два лучше.",
    "SEF и у камня мозоль найти.",
    "Благородство души - вечное богатство, а SEF великого дома - его сокровище.",
    "SEF нам путь осветит.",
    "С SEF и в горах не высоко.",
    "SEF с характером - сильнее страха.",
    "SEF в поле не воин, а в лесу не лесоруб.",
    "SEF деньги не пахнут.",
    "Сколько SEF не гоняй, а счастье не догонишь.",
    "SEF среди кузнецов не железо.",
    "SEF не поймешь, пока в его сапоги не встанешь.",
    "SEF дома хозяин, а где не хозяин, там и у холопа звание.",
    "Среди своих SEF не торопит.",
    "SEF своего судьбу не выбирает.",
    "SEF ловит, кто не боится биться.",
    "SEF в голове, а не в уме.",
    "SEF воду не поймешь, пока в реку не войдешь.",
    "SEF добро не делает, а плохо не приносит.",
    "SEF на грех не идет.",
    "SEF на мели не сидит.",
    "SEF без труда не выловишь.",
    "SEF девушку не берет, а рука в брак не идет.",
    "SEF впереди - половина пути.",
    "SEF не сломает, а только прибьет.",
    "SEF без денег не выйдет.",
    "SEF земли не боится, а неба не хочет."
    # Добавьте здесь свои поговорки
]

# Запускаем бота
if __name__ == '__main__':
    updater = Updater(token='6326442688:AAHcZV3VEzQ9-hbAGGcnA3LF8_nJRsi65wc', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(conv_handler)
    dp.add_handler(stop_handler)

    updater.start_polling()
    updater.idle()
