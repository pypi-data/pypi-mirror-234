import datetime


class log:
    message_width = 70

    @classmethod
    def __get_date(cls):
        format = "%H:%M:%S %d/%m"
        return datetime.datetime.now().strftime(format)

    @classmethod
    def info(cls, msg: str):
        log_msg = f"{'INFO':<10} {msg.ljust(cls.message_width)} {cls.__get_date()} [+]"
        print(log_msg)

    @classmethod
    def warning(cls, msg: str):
        log_msg = f"{'WARNING':<10} {msg.ljust(cls.message_width)} {cls.__get_date()} <"
        print(log_msg)

    @classmethod
    def error(cls, msg: str):
        log_msg = f"{'ERROR':<10} {msg.ljust(cls.message_width)} {cls.__get_date()} <<<"
        print(log_msg)

    @classmethod
    def debug(cls, msg: str):
        log_msg = f"{'DEBUG':<10} {msg.ljust(cls.message_width)} {cls.__get_date()}"
        print(log_msg)