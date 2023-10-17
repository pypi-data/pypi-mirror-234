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
        Style.minecraft("&","&l&ahello &r&5world&e!&r")\n
        Style.minecraft("§l§ahello §r§5world§e!§r")
        '''
        symbol = "§"

        codes = {
            f"0": Color.text("#000"),
            f"1": Color.text("#00a"),
            f"2": Color.text("#0a0"),
            f"3": Color.text("#0aa"),
            f"4": Color.text("#a00"),
            f"5": Color.text("#a0a"),
            f"6": Color.text("#fa0"),
            f"7": Color.text("#aaa"),
            f"8": Color.text("#555"),
            f"9": Color.text("#55f"),
            f"a": Color.text("#5f5"),
            f"b": Color.text("#5ff"),
            f"c": Color.text("#f55"),
            f"d": Color.text("#f5f"),
            f"e": Color.text("#ff5"),
            f"f": Color.text("#fff"),
            f"l": Style.bold(),
            f"m": Style.strikethrough(),
            f"n": Style.underline(),
            f"o": Style.italic(),
            f"r": Style.reset()
            }

        if len(args) == 2:
            symbol, text = args
            for key, value in codes.items():
                text = text.replace(symbol+key, value)

        if len(args) == 1:
            text = args
            for key, value in codes.items():
                text = text.replace(symbol+key, value)
        return text
    
class Color:
    @staticmethod
    def text(*args):
        '''
        changes the color of the text\n
        Color.text(r, g, b)\n
        Color.text("#rrggbb")
        '''
        if len(args) == 1:
            color = args[0].lstrip("#")
            if len(color) == 3:
                r, g, b = (int(c * 2, 16) for c in color)
            elif len(color) == 6:
                r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
            else:
                raise ValueError("Invalid color format")
        elif len(args) == 3:
            r, g, b = args
        else:
            raise ValueError("Invalid number of arguments")

        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def background(*args):
        '''
        changes the color of the text background\n
        Color.background(r, g, b)\n
        Color.background("#rrggbb")
        '''
        if len(args) == 1:
            color = args[0].lstrip("#")
            if len(color) == 3:
                r, g, b = (int(c * 2, 16) for c in color)
            elif len(color) == 6:
                r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
            else:
                raise ValueError("Invalid color format")
        elif len(args) == 3:
            r, g, b = args
        else:
            raise ValueError("Invalid number of arguments")

        return f"\033[48;2;{r};{g};{b}m"
