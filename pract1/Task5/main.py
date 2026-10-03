from logger import Logger


def main():
    log1 = Logger("LogiMakca.log")
    log2 = Logger("LogiTelegrama.log")
    print(log1 is log2)
    print(log2.filename)
    log1.debug("Добавьте чаты пж молю")
    log1.info("Что будет, если нажать drop database?")
    log2.critical("Мы слили всю датубазу")
    log1.critical("А тепернь ещё и дропнули")


if __name__ == '__main__':
    main()