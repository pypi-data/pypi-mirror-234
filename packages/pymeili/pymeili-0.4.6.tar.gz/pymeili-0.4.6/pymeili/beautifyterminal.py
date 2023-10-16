# 前景色: 30:黑 31:红 32:绿 33:黄 34:蓝色 35:紫色 36:深绿 37:白色
class fg:
    PURPLE = '\033[95m' # purple
    BLUE = '\033[94m' # blue
    CYAN = '\033[96m' # cyan

    GREEN = '\033[92m' # green
    YELLOW = '\033[93m' # yellow
    RED = '\033[91m' # red
    WHITE = '\033[0m' # white
    BOLD = '\033[1m' # bold
    UNDERLINE = '\033[4m' # underline

# 背景色: 40:黑 41:红 42:绿 43:黄 44:蓝色 45:紫色 46:深绿 47:白色
class bg:
    PURPLE = '\033[45m' # purple
    BLUE = '\033[44m' # blue
    CYAN = '\033[46m' # cyan

    GREEN = '\033[42m' # green
    YELLOW = '\033[43m' # yellow
    RED = '\033[41m' # red
    WHITE = '\033[47m' # white

DEFAULT = '\033[0m'

# accept multiple arguments
def bprint(text, *style, end='\n', sep=' '):
    if len(style) == 0:
        print(text, end=end, sep=sep)
    else:
        print(''.join(style) + text + fg.WHITE, end=end, sep=sep)

def inspectfg():
    print(fg.PURPLE + 'fg.PURPLE' + DEFAULT)
    print(fg.BLUE + 'fg.BLUE' + DEFAULT)
    print(fg.CYAN + 'fg.CYAN' + DEFAULT)
    print(fg.GREEN + 'fg.GREEN' + DEFAULT)
    print(fg.YELLOW + 'fg.YELLOW' + DEFAULT)
    print(fg.RED + 'fg.RED' + DEFAULT)
    print(fg.WHITE + 'fg.WHITE' + DEFAULT)
    print(fg.BOLD + 'fg.BOLD' + DEFAULT)
    print(fg.UNDERLINE + 'fg.UNDERLINE' + DEFAULT)

def inspectbg():
    print(bg.PURPLE + 'bg.PURPLE' + DEFAULT)
    print(bg.BLUE + 'bg.BLUE' + DEFAULT)
    print(bg.CYAN + 'bg.CYAN' + DEFAULT)
    print(bg.GREEN + 'bg.GREEN' + DEFAULT)
    print(bg.YELLOW + 'bg.YELLOW' + DEFAULT)
    print(bg.RED + 'bg.RED' + DEFAULT)
    print(bg.WHITE + 'bg.WHITE' + DEFAULT)

def upgrade():
    import os
    os.system('pip install --upgrade pymeili')