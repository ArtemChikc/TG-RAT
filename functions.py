import platform
import psutil
from tabulate import tabulate
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.messagebox import *
import re
import soundfile as sf
import sounddevice as sd
import ctypes
import subprocess
import cv2
import numpy as np
import pyautogui as pag
import os
import time



def vid_capture(video_filename, fps, duration):
    screen_size = pag.size()

    for i in range(5):
        webcam = cv2.VideoCapture(i)
        if webcam.isOpened():
            break
    webcam_width = int(screen_size.width * 0.25)
    webcam_height = int(screen_size.height * 0.3)

    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"mp4v"), fps, screen_size)

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

    return open(video_filename, "rb")



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



def open_win(file_name):
    image = Image.open(file_name)
    image_width, image_height = image.size
    root = tk.Tk()
    root.resizable(0, 0)
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(True)
    root.geometry(f"{image_width}x{image_height}+{(root.winfo_screenwidth()-image_width)//2}+{(root.winfo_screenheight()-image_height)//2}")
    tk_image = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=tk_image)
    label.pack()
    label.bind("<Button-1>", lambda event: root.destroy())
    root.mainloop()

def play_sound(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

def change_wallpaper(image_path):
    system = platform.system().lower()
    if system == "windows":
        return _change_wallpaper_windows(image_path)
    elif system == "darwin":
        return _change_wallpaper_macos(image_path)
    elif system == "linux":
        return _change_wallpaper_linux(image_path)

def _change_wallpaper_windows(image_path): # Изменение обоев для Windows
    try:
        abs_path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        return f"Обои успешно изменены: {abs_path}"
    except Exception as e:
        return f"Ошибка при изменении обоев в Windows: {e}"

def _change_wallpaper_macos(image_path): # Изменение обоев для macOS
    try:
        abs_path = os.path.abspath(image_path)
        script = f'''
        tell application "System Events"
            set picture of every desktop to "{abs_path}"
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Обои успешно изменены: {abs_path}"
    except Exception as e:
        return f"Ошибка при изменении обоев в macOS: {e}"

def _change_wallpaper_linux(image_path): # Изменение обоев для Linux
    try:
        abs_path = os.path.abspath(image_path)
        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        if "gnome" in desktop_env or "ubuntu" in desktop_env:
            # GNOME, Unity
            subprocess.run([
                "gsettings", "set", 
                "org.gnome.desktop.background", 
                "picture-uri", 
                f"file://{abs_path}"
            ], check=True)
        elif "kde" in desktop_env:
            # KDE Plasma
            subprocess.run([
                "plasma-apply-wallpaperimage", abs_path
            ], check=True)
        elif "xfce" in desktop_env:
            # XFCE
            subprocess.run([
                "xfconf-query", "-c", "xfce4-desktop", 
                "-p", "/backdrop/screen0/monitor0/image-path", 
                "-s", abs_path
            ], check=True)
        else:
            # Универсальный метод (может не работать везде)
            subprocess.run([
                "feh", "--bg-scale", abs_path
            ], check=True)
        return f"Обои успешно изменены: {abs_path}"
    except Exception as e:
        return f"Ошибка при изменении обоев в Linux: {e}"


def set_system_cursor(cursor_path): # Изменяет системный курсор мыши (только Windows)
    try:
        cursor_handle = ctypes.windll.user32.LoadImageW(
            0,  # hInstance (0 для загрузки из файла)
            cursor_path,  # путь к файлу
            2,  # IMAGE_CURSOR
            0,  # ширина (0 - авто)
            0,  # высота (0 - авто)
            0x0010  # LR_LOADFROMFILE
        )
        if cursor_handle:
            ctypes.windll.user32.SetSystemCursor(cursor_handle, 32512) # OCR_NORMAL
            return f"Системный курсор изменен: {cursor_path}"
        else:
            return "Не удалось загрузить курсор"
    except Exception as e:
        print(f"Ошибка изменения системного курсора: {e}")
        return False

def restore_system_cursor(): # Восстанавливает стандартный системный курсор
    try:
        ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, 0, 0) # SPI_SETCURSORS
        return "Системный курсор восстановлен"
    except Exception as e:
        return f"Ошибка восстановления курсора: {e}"