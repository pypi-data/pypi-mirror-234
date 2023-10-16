<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap" rel="stylesheet">

<span style="color:#fff; font-family: quicksand;">

# Chroma Console

Chroma console is a python package for adding color and style to terminal text output using ANSI escape codes.

## Installation

```shell
pip install chromaconsole
```

## Functions
```python
Style.bold()
Style.italic()
Style.underline()
Style.strikethrough()
Style.negative()
Style.normal()
Style.reset()
Style.minecraft(*args)
Color.text(*args)
Color.background(*args)
```

## Example usage

```python
from chromaconsole import Color, Style

print(f"{Color.text(r, g, b)}here is RGB colored text{Style.reset()}")
print(f"{Color.background(r, g, b)}here is RGB colored background{Style.reset()}")

print(f"{Color.text('#rrggbb')}here is HEX colored text{Style.reset()}")
print(f"{Color.background('#rrggbb')}here is HEX colored background{Style.reset()}")

print(f"{Style.bold()}Bold {Style.reset()}")
print(f"{Style.italic()}Italic {Style.reset()}")
print(f"{Style.underline()}Underline {Style.reset()}")
print(f"{Style.strikethrough()}Strikethrough {Style.reset()}")

print(f"{Style.bold()}{Style.italic()}bold+italic {Style.reset()}")
print(f"{Style.minecraft('§','§ahello §4world§r')}")
```
</span>