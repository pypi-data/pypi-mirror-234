import random


class bcolors:
    ENDC = '\033[0m'

    BOLD = '\033[1m'
    DARK = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    CONCEALED = '\033[8m'

    WHITE = '\033[97m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'

    LIGHT_GREY = '\033[37m'
    DARK_GREY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'

    HIGHLIGHTS_WHITE = '\033[107m'
    HIGHLIGHTS_BLACK = '\033[40m'
    HIGHLIGHTS_RED = '\033[41m'
    HIGHLIGHTS_GREEN = '\033[42m'
    HIGHLIGHTS_YELLOW = '\033[43m'
    HIGHLIGHTS_BLUE = '\033[44m'
    HIGHLIGHTS_MAGENTA = '\033[45m'
    HIGHLIGHTS_CYAN = '\033[46m'

    HIGHLIGHTS_LIGHT_GREY = '\033[47m'
    HIGHLIGHTS_DARK_GREY = '\033[100m'
    HIGHLIGHTS_LIGHT_RED = '\033[101m'
    HIGHLIGHTS_LIGHT_GREEN = '\033[102m'
    HIGHLIGHTS_LIGHT_YELLOW = '\033[103m'
    HIGHLIGHTS_LIGHT_BLUE = '\033[104m'
    HIGHLIGHTS_LIGHT_MAGENTA = '\033[105m'
    HIGHLIGHTS_LIGHT_CYAN = '\033[106m'

    @staticmethod
    def format_text(text, color, highlights=None, attributes: list = None, end: bool = False):
        return f'{color}{highlights if highlights is not None else ""}' \
               f'{"".join(attributes) if attributes is not None and len(attributes) > 0 else ""}' \
               f'{text}{bcolors.ENDC if end is not None else ""}'


class wcolors:
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)

    GREEN_LIME = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    GREEN = (0, 128, 0)
    RED_DARK = (128, 0, 0)
    BLUE_DARK = (0, 0, 128)

    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)

    PURPLE = (128, 0, 128)
    OLIVE = (128, 128, 0)
    TEAL = (0, 128, 128)

    ORANGE = (255, 165, 0)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)
    VIOLET = (238, 130, 238)

    GRAY_IRON = (82, 89, 93)
    GRAY_DIM = (105, 105, 105)
    GRAY_DARK = (169, 169, 169)
    GRAY_LIGHT = (211, 211, 211)
    ORANGE_DARK = (255, 140, 0)
    PINK_DEEP = (255, 20, 147)
    BROWN_SAND = (244, 164, 96)
    BROWN_SADDLE = (139, 69, 19)
    PURPLE_INDIGO = (75, 0, 130)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    BLUE_AZURE = (0, 127, 255)
    GREEN_DARK = (0, 100, 0)

    @staticmethod
    def random():
        return tuple(random.randint(0, 255) for _ in range(3))
