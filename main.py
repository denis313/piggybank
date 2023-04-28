from telebot import types
from bot.loader import bot
import bd


@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.chat.id
    k_b = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Пополнить')
    btn2 = types.KeyboardButton(text='Новая операция')
    btn3 = types.KeyboardButton(text='Узнать баланс')
    btn4 = types.KeyboardButton(text='Поиск проведенных операций')
    # btn5 = types.KeyboardButton(text='Удалить историю')
    k_b.add(btn1, btn2, btn3, btn4)
    bot.send_message(user_id, f"Привет {message.from_user.first_name}, "
                              f"этот Бот позволяет следить за финансами", bd.registration(message), reply_markup=k_b)


@bot.message_handler(content_types=['text'])
def keyboard(message):
    user_id = message.chat.id
    text = message.text
    if text == 'Новая операция':
        msg = bot.send_message(user_id, "ДОБАВЛЕНИЕ НОВЫХ ТРАТ:\n"
                                    "Пример: Еда Кола 200")
        bot.register_next_step_handler(msg, bd.new_purchase)
    if text == 'Пополнить':
        msg = bot.send_message(user_id, "Введите название и сумму пополнения счета\n"
                                    "Пример: 60000")
        bot.register_next_step_handler(msg, bd.up_balance)

    if text == 'Узнать баланс':
        bot.send_message(user_id, f"Баланс: {round(bd.select_balance(user_id)[-1][0], 2)}")

    if text == 'Поиск проведенных операций':
        msg = bot.send_message(user_id, 'Введите категорию для поиска')
        bot.register_next_step_handler(msg, bd.category_amount)

    # if text == 'Удалить историю':
    #     bot.send_message(user_id, 'История за прошлый месяц удалена :)')
    #     bd.job()


@bot.callback_query_handler(func=lambda c: c.data)
def key_call(callback):
    if callback.data == callback.data:
        bot.send_message(callback.message.chat.id, bd.all_operations(callback))


bot.infinity_polling(skip_pending=True)
