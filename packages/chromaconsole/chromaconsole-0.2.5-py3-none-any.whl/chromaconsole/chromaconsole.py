class Style:
    @staticmethod
    def bold():
        return "\033[1m"

    @staticmethod
    def italic():
        return "\033[3m"

    @staticmethod
    def underline():
        return "\033[4m"
    
    @staticmethod
    def strikethrough():
        return "\033[9m"
    
    @staticmethod
    def dimmer():
        return "\033[2m"
    
    @staticmethod
    def normal():
        return "\033[22m"
    
    @staticmethod
    def reset():
        return "\033[0m"
    
    @staticmethod
    def minecraft(*args):
        symbol = "§"

        codes = {
            f"{symbol}0": Color.text("#000000"),
            f"{symbol}1": Color.text("#0000aa"),
            f"{symbol}2": Color.text("#00aa00"),
            f"{symbol}3": Color.text("#00aaaa"),
            f"{symbol}4": Color.text("#aa0000"),
            f"{symbol}5": Color.text("#aa00aa"),
            f"{symbol}6": Color.text("#ffaa00"),
            f"{symbol}7": Color.text("#aaaaaa"),
            f"{symbol}8": Color.text("#555555"),
            f"{symbol}9": Color.text("#5555ff"),
            f"{symbol}a": Color.text("#55ff55"),
            f"{symbol}b": Color.text("#55ffff"),
            f"{symbol}c": Color.text("#ff5555"),
            f"{symbol}d": Color.text("#ff55ff"),
            f"{symbol}e": Color.text("#ffff55"),
            f"{symbol}f": Color.text("#ffffff"),
            f"{symbol}l": Style.bold(),
            f"{symbol}m": Style.strikethrough(),
            f"{symbol}n": Style.underline(),
            f"{symbol}o": Style.italic(),
            f"{symbol}r": Style.reset()
            }

        if len(args) == 2:
            symbol, text = args
            for key, value in codes.items():
                text = text.replace(key, value)
        return text

class Color:
    @staticmethod
    def text(*args):
        r, g, b = args if len(args) == 3 else tuple(int(args[0].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def background(*args):
        r, g, b = args if len(args) == 3 else tuple(int(args[0].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[48;2;{r};{g};{b}m"