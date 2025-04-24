import logging
from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    def __init__(self, base_formatter: logging.Formatter):
        super().__init__()
        self.base_formatter = base_formatter

    def format(self, record: logging.LogRecord) -> str:
        # Define colors for each log level
        level_colors = {
            logging.DEBUG: Fore.CYAN,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
        }
        color = level_colors.get(record.levelno, Fore.WHITE)
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return self.base_formatter.format(record)


class CustomLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        super().__init__(name, level)
        self.setLevel(level)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            fmt="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%d-%m %H:%M:%S",
        )

        # Add formatter to console handler
        ch.setFormatter(ColoredFormatter(formatter))

        # Add console handler to logger
        self.addHandler(ch)


if __name__ == "__main__":
    logger = CustomLogger(name="MyFancyLogger")
    logger.info("This is an info message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
