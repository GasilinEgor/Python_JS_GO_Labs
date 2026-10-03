from datetime import datetime


class Logger:
    _instance  = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename):
        if getattr(self, '_initialized', False):
            return
        self._filename = filename
        self._initialized = True
    
    @property
    def filename(self):
        return self._filename
    
    def write(self, status, message):
        log_time = datetime.now().strftime("%d-%m-%Y %S:%M:%H")
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(f'[{status}] {log_time}: {message}\n')

    def debug(self, message):
        self.write("DEBUG", message) 
    
    def info(self, message):
        self.write("INFO", message) 
    
    def warn(self, message):
        self.write("WARN", message) 
    
    def error(self, message):
        self.write("ERROR", message) 
    
    def critical(self, message):
        self.write("CRITICAL", message) 