class Style:
    @staticmethod
    def bold():
        '''
        makes the text bold
        '''
        return "\033[1m"

    @staticmethod
    def italic():
        '''
        makes the text italic
        '''
        return "\033[3m"

    @staticmethod
    def underline():
        '''
        makes the text underlined
        '''
        return "\033[4m"
    
    @staticmethod
    def strikethrough():
        '''
        makes the text strikethrough
        '''
        return "\033[9m"
    
    @staticmethod
    def negative():
        """
        inverts the text colors
        """
        return "\033[7m"
        
    # end def
    
    @staticmethod
    def normal():
        '''
        resets the style of the text
        '''
        return "\033[22m"
    
    @staticmethod
    def reset():
        '''
        resets style and color of the text
        '''
        return "\033[0m"
    
    @staticmethod
    def minecraft(*args):
        '''
        converts minecraft styled text to colored text\n
        Style.minecraft("§","§l§ahello §r§5world§e!§r")
        '''
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
        '''
        changes the color of the text\n
        Color.text(r, g, b)\n
        Color.text("#rrggbb")
        '''
        r, g, b = args if len(args) == 3 else tuple(int(args[0].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def background(*args):
        '''
        changes the color of the text background\n
        Color.background(r, g, b)\n
        Color.background("#rrggbb")
        '''
        r, g, b = args if len(args) == 3 else tuple(int(args[0].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[48;2;{r};{g};{b}m"