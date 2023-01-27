import telebot
import main

TOKEN = 'MYTOKENHERE'
bot = telebot.TeleBot(TOKEN)
cnt = 0



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот, переносящий стиль одного изображения на другое. Пожалуйста, отправь вначале изображение, на котором хочешь поменять стиль, а затем изображение с нужным стилем. Разрешение картинки должно быть больше 512 пикселей")


@bot.message_handler()
def send_answ(content_img, style_img, input_img, message):
    output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                content_img, style_img, input_img)
    out_img = open(output, 'rb')
    bot.send_photo(message.chat.id, out_img)


@bot.message_handler(content_types=['photo'])
def photo(message):
    global cnt, content_img, style_img
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = open(name, 'rb')
    if cnt % 2 == 0:
        content_img = img
        content_img = image_loader(content_img)
        bot.send_message(message.chat.id, "Картинка контента получена")
    else:
        style_img = img
        style_img = image_loader(style_img)
        bot.send_message(message.chat.id, "Картинка стиля получена")
    cnt += 1
    if cnt != 0 and cnt % 2 == 0:
        bot.send_message(message.chat.id, "Подождите около 30 секунд, пожалуйста")
        output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                content_img, style_img, content_img)
        out_img = output.squeeze(0)
        out_img = unloader(out_img)
        bot.send_photo(message.chat.id, out_img)
        bot.send_message(message.chat.id, "Жду следующих картинок")




bot.polling(none_stop=True)