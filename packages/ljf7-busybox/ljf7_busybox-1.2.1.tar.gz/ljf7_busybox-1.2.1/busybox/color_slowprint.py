from busybox.slowprint import slowprint
from colorama import Fore

def color_slowprint(s, color):
    if color == 'red':
        slowprint(Fore.RED + s + '\n')
    elif color ==  'green':
        slowprint(Fore.GREEN + s + '\n')
    elif color == "yellow":
        slowprint(Fore.YELLOW + s + '\n')
    elif color == 'blue':
        slowprint(Fore.BLUE + s + '\n')
    elif color == 'magenta':
        slowprint(Fore.MAGENTA + s + '\n')
    elif color == 'white':
        slowprint(Fore.WHITE + s + '\n')
    else:
        slowprint(Fore.BLACK + s + '\n')

# test example:
# color_slowprint("Hello World", "red")
# color_slowprint("Hello World", "blue")
# color_slowprint("Hello World", "green")