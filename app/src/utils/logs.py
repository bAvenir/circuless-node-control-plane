import logging
import sys

class ColorfulLevelnameFormatter(logging.Formatter):
    # ANSI escape codes for background colors
    BG_COLORS = {
        "DEBUG": "\033[44m",    # Blue background
        "INFO": "\033[42m",     # Green background
        "WARNING": "\033[43m",  # Yellow background
        "ERROR": "\033[41m",    # Red background
        "CRITICAL": "\033[45m", # Magenta background
    }
    RESET = "\033[0m"

    def format(self, record):
        levelname = record.levelname
        bg_color = self.BG_COLORS.get(levelname, "")
        colored_levelname = f"{bg_color}{" " + levelname + " "}{self.RESET}"
        record.levelname = colored_levelname
        return super().format(record)
    
def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Application-wide level

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = ColorfulLevelnameFormatter('     %(levelname)s %(asctime)s - %(name)s:%(lineno)d - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Reduce SQLAlchemy verbosity here
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)

    return logger