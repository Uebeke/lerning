import telebot
from telebot import types
from string import Template

bot = telebot.TeleBot("1582525923:AAH4t4mUPM6HTiLamN3uZwZEnxuaAfEBC3U", parse_mode='html')

user_dict = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'location', 
                'suggestions']
        
        for key in keys:
            self.key = None

#ответ при запуске
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    #создание клавиатуры 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('как проходит съемка?')
    item2 = types.KeyboardButton('узнать прайс')
    item3 = types.KeyboardButton('связаться со мной')
    item4 = types.KeyboardButton('записаться на съемку')

    #добавляем кнопки
    markup.add(item1, item2, item3, item4)

    #привественное сообщение
    bot.send_message(message.chat.id, "привет,меня зовут злата, я твой polaroid фотограф. я хочу предоставить тебе возможность сохранить твои самые любимые фотокарточки не только в пикселях, но и на бумаге.", reply_markup=markup)
   

@bot.message_handler(func=lambda m: True)
def otvet(message):
    if message.text == "как проходит съемка?":
        bot.send_message(message.chat.id, "мы решаем где будет проходить съёмка в студии или нет, после чего выбираем локацию. если это необходимо, я помогаю составить образы, присылаю референсы, в процессе съёмки помогаю с позированием.\nсама съёмка осуществляется на профессиональный зеркальный фотоаппарат Nikon D7200. после съёмки детально обрабатываются /цветокоррекция и ретушь/ 10 фото, 5 из которых печатаются на polaroid.")   
    elif message.text == "узнать прайс":
        bot.send_message(message.chat.id, "25ОО руб.\n\n‘10 фото в детальной обработке в цифровом формате\n‘5 фото на выбор в детальной обработке на polaroid\n‘помощь с подбором образа и локации\n\n*студия оплачивается отдельно\n*дополнительное фото на polaroid 1ОО руб.")

    elif message.text == "связаться со мной":
        bot.send_message(message.chat.id, "для связи:\nVK - zlataslv\nTG - @zlataslv\nINST - zlata.slv")
    elif message.text == "записаться на съемку": 
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        markup1 = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "укажите, пожалуйста, ваше имя", reply_markup=markup1)
        bot.register_next_step_handler(msg, process_name_step) 
    else:
        bot.send_message(message.chat.id, "я не понимаю. попробуйте еще раз.")  

def process_name_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'введите ваш номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'попробуй еще раз')

def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('в студии')
        item2 = types.KeyboardButton('вне студии')
        item3 = types.KeyboardButton('пока не знаю')

        markup.add(item1, item2, item3)

        msg = bot.send_message(chat_id, 'где бы вы хотели провести съемку?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_location_step)
    except Exception as e:
        bot.reply_to(message, 'попробуй еще раз')

def process_location_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.location = message.text

        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'напишите пожелания по съемке', reply_markup=markup)
        bot.register_next_step_handler(msg, process_suggestions_step)

    except Exception as e:
        bot.reply_to(message, 'попробуй еще раз')

def process_suggestions_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.suggestions = message.text
        grup_id = "-1001180411414"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('как проходит съемка?')
        item2 = types.KeyboardButton('узнать прайс')
        item3 = types.KeyboardButton('связаться со мной')
        item4 = types.KeyboardButton('записаться на съемку')
        markup.add(item1, item2, item3, item4)

        bot.send_message(chat_id, getRegData(user, 'ваша заявка,', message.from_user.first_name), parse_mode="Markdown")
        bot.send_message(grup_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")
        bot.send_message(message.chat.id, "в ближайшее время я свяжусь с вами для уточнения деталей", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, 'попробуй еще раз')

def getRegData(user, title, name):
    t = Template('$title *$name* \nимя: *$fullname* \nтелефон: *$phone* \nместо: *$location* \nпожелания: *$suggestions* \n')

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'phone': user.phone,
        'location': user.location,
        'suggestions': user.suggestions,
    })

  
    #5. в ближайшее время я с вами свяжусь для уточнения деталей
    #6. реализовать ответ от имени бота
    #7. вернуть кнопки первичного управления 
if __name__ == '__main__':
    bot.polling(none_stop=True)