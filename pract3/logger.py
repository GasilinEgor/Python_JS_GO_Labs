import logging


def setup(log_file: str) -> logging.Logger:
    logger = logging.getLogger("db_generator")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger