import platform
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from colorama import init, Fore, Back, Style
init(autoreset=True)


plat = platform.system()


color_front_codes = {"red": 31, "black": 30, "green": 32, "yellow": 33, "blue": 34, 'magenta': 35, "cyan": 36,
                     "white": 37, "ordinary": 38}
color_back_codes = {"red": 41, "black": 40, "green": 42, "yellow": 43, "blue": 44, 'magenta': 45, "cyan": 46,
                    "white": 47, "ordinary": 48}
color_show_modes = {"default": 0, "highlight": 1, "non-highlight": 22, "underline": 4, "non_underline": 24,
                    "blinking": 5, "non-blinking": 25, "reverse": 7, "non-reverse": 27, "invisible": 8, 'visible': 28}

win_back_color_map = {
    "red": Back.RED,
    "black": Back.BLACK,
    "green": Back.GREEN,
    "yellow": Back.YELLOW,
    "blue": Back.BLUE,
    'magenta': Back.MAGENTA,
    "cyan": Back.CYAN,
    "white": Back.WHITE,
    "ordinary": Back.RESET,
    None: Back.RESET,
}
win_font_color_map = {
    "red": Fore.RED,
    "black": Fore.BLACK,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    'magenta': Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "ordinary": Fore.RESET,
    None: Fore.RESET,
}
win_show_modes = {
    "default": Style.RESET_ALL,
    "highlight": Style.BRIGHT,
}


def color(txt, show_mode=None, back_color=None, front_color=None):
    """
    自己配色
    :param txt: 需要上色的文本
    :param show_mode: 显示模式，加深或闪耀等
    :param back_color: 背景色
    :param front_color: 字体颜色
    :return: 返回上色后的文本
    提示：在一些终端可能无法显示，例如 windows
    """
    if plat in {"Linux", "Darwin"}:
        show_mode = color_show_modes.get(show_mode, 0)
        back_code = color_back_codes.get(back_color, 48)
        front_code = color_front_codes.get(front_color, 38)
        return f"\033[{show_mode};{front_code};{back_code}m{txt}\033[0m"
    else:
        return txt


def print_color(txt, show_mode=None, back_color=None, front_color=None, no_end=False):
    """
    自己配色
    :param txt: 需要上色的文本
    :param show_mode: 显示模式，加深或闪耀等
    :param back_color: 背景色
    :param front_color: 字体颜色
    :param no_end: not end
    :return: 返回上色后的文本
    提示：在一些终端可能无法显示，例如 windows
    """
    if plat in {"Linux", "Darwin"}:
        show_mode = color_show_modes.get(show_mode, 0)
        back_code = color_back_codes.get(back_color, 48)
        front_code = color_front_codes.get(front_color, 38)
        print(f"\033[{show_mode};{front_code};{back_code}m{txt}\033[0m")
    elif plat == "Windows":
        print_txt = ""
        if show_mode == 'highlight':
            print_txt += Style.BRIGHT
        if front_color:
            print_txt += win_font_color_map.get(front_color) or Fore.RESET
        if back_color:
            print_txt += win_back_color_map.get(back_color) or Back.RESET
        if not no_end:
            print(print_txt + txt)
        else:
            print(print_txt + txt, end='')
    else:
        print(f"Unknown Platform: [ {plat} ]")


def wait(rw):
    print()
    while rw >= 0:
        m, s = divmod(rw, 60)
        h, m = divmod(m, 60)
        print(f'countdown [ {color(f"{h}:{m}:{s}", show_mode="blinking", front_color="red")} ]\r', end='')
        rw -= 1
        sleep(1)
    print()


def show_all(effect=True):
    """
    展示所有的颜色名称和代号
    :param effect: 是否显示效果
    :return: 终端打印效果或代号
    提示：在一些终端可能无法显示，例如 windows
    """
    max_len = 21
    try:
        import os
        length = os.get_terminal_size().columns
    except:
        length = 200
    base = "%s%s,%s%s"
    
    if plat in {"Linux", "Darwin"}:
        if not effect:
            head = ("{:%s%s%s}" % ('=', '^', length)).format(" no effect ")
            print(head)
            print("show modes: ",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in color_show_modes.items()]))
            print("front codes:",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in color_front_codes.items()]))
            print("back codes: ",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in color_back_codes.items()]))
            print("=" * length)
            return
    
        print_str = "\n将显示所有的颜色效果组合，每个显示模式（show_mode）为一组\n左对角线字体不显示，因为字体颜色和背景色一致了，可以尝试加上 -ne 参数去除效果\n\n"
        for i in print_str:
            sys.stdout.write(i)
            sys.stdout.flush()
            sleep(0.03)
        wait(5)
        for sc_name in color_show_modes:
            sc = color_show_modes.get(sc_name)
            head = f" in mode: {sc_name}, code: {sc} "
            head = ("{:%s%s%s}" % ('=', '^', length)).format(head)
            print(head)
            for bc_name, bc in color_back_codes.items():
                li = [
                    color(f"{base % (fc_name, fc, bc_name, bc)}{' ' * (max_len - len(base % (fc_name, fc, bc_name, bc)))}",
                          sc_name, bc_name, fc_name)
                    for fc_name, fc in color_front_codes.items()]
                print(" ".join(li))
            print("=" * length)
            print()
            print()
    elif plat == "Windows":
        if not effect:
            head = ("{:%s%s%s}" % ('=', '^', length)).format(" no effect ")
            print(head)
            print("show modes: ",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in win_show_modes.items()]))
            print("front codes:",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in win_font_color_map.items()]))
            print("back codes: ",
                  " ".join([("{:%s%s%s}" % (' ', '<', 16)).format(f"{k}:{v}") for k, v in win_back_color_map.items()]))
            print("=" * length)
            return

        print_str = "\n将显示所有的颜色效果组合，每个显示模式（show_mode）为一组\n左对角线字体不显示，因为字体颜色和背景色一致了，可以尝试加上 -ne 参数去除效果\n\n"
        for i in print_str:
            sys.stdout.write(i)
            sys.stdout.flush()
            sleep(0.03)
        wait(5)
        for sc_name in win_show_modes:
            sc = win_show_modes.get(sc_name)
            head = f" in mode: {sc_name}, mode name: {sc} "
            head = ("{:%s%s%s}" % ('=', '^', length)).format(head)
            print(head)
            for bc_name, bc in win_back_color_map.items():
                for fc_name, fc in win_font_color_map.items():
                    txt = f"{base % (fc_name, fc, bc_name, bc)}{' ' * (max_len - len(base % (fc_name, fc, bc_name, bc)))} "
                    print_color(txt, sc_name, bc_name, fc_name, no_end=True)
                print()
            print("=" * length)
            print()
            print()
    else:
        print(f"Unknown Platform: [ {plat} ]")


def red(txt, with_bgc=None):
    """
    普通红色
    :param with_bgc: 需要添加的背景色，默认不显示
    :param txt:
    :return:
    """
    if plat != "Windows":
        return color(txt, "default", with_bgc or "ordinary", "red")
    else:
        return txt


def print_red(txt, with_bgc=None, no_end=False):
    """
    普通红色
    :param with_bgc: 需要添加的背景色，默认不显示
    :param txt:
    :param no_end:
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "red"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.RED + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)

def green(txt, with_bgc=None):
    """
    普通绿色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "default", with_bgc or "ordinary", "green")
    else:
        return txt


def print_green(txt, with_bgc=None, no_end=False):
    """
    普通绿色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "green"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.GREEN + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def yellow(txt, with_bgc=None):
    """
    普通黄色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "default", with_bgc or "ordinary", "yellow")
    else:
        return txt


def print_yellow(txt, with_bgc=None, no_end=False):
    """
    普通黄色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "yellow"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.YELLOW + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def blue(txt, with_bgc=None):
    """
    普通蓝色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "default", with_bgc or "ordinary", "blue")
    else:
        return txt


def print_blue(txt, with_bgc=None, no_end=False):
    """
    普通蓝色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "blue"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.BLUE + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def magenta(txt, with_bgc=None):
    """
    普通品红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "default", with_bgc or "ordinary", "magenta")
    else:
        return txt


def print_magenta(txt, with_bgc=None, no_end=False):
    """
    普通品红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "magenta"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.MAGENTA + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def cyan(txt, with_bgc=None):
    """
    普通青色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "default", with_bgc or "ordinary", "cyan")
    else:
        return txt


def print_cyan(txt, with_bgc=None, no_end=False):
    """
    普通青色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "default", with_bgc or "ordinary", "cyan"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.CYAN + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hcyan(txt, with_bgc=None):
    """
    加深青色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "cyan")
    else:
        return txt


def print_hcyan(txt, with_bgc=None, no_end=False):
    """
    加深青色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "cyan"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.CYAN + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hblue(txt, with_bgc=None):
    """
    加深蓝色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "blue")
    else:
        return txt


def print_hblue(txt, with_bgc=None, no_end=False):
    """
    加深蓝色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "blue"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.BLUE + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hmagenta(txt, with_bgc=None):
    """
    加深品红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "magenta")
    else:
        return txt


def print_hmagenta(txt, with_bgc=None, no_end=False):
    """
    加深品红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "magenta"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.MAGENTA + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hyellow(txt, with_bgc=None):
    """
    加深黄色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "yellow")
    else:
        return txt


def print_hyellow(txt, with_bgc=None, no_end=False):
    """
    加深黄色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "yellow"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.YELLOW + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hgreen(txt, with_bgc=None):
    """
    加深绿色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "green")
    else:
        return txt


def print_hgreen(txt, with_bgc=None, no_end=False):
    """
    加深绿色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "green"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.GREEN + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def hred(txt, with_bgc=None):
    """
    加深红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        return color(txt, "highlight", with_bgc or "ordinary", "red")
    else:
        return txt


def print_hred(txt, with_bgc=None, no_end=False):
    """
    加深红色
    :param txt:
    :param with_bgc: 需要添加的背景色，默认不显示
    :return:
    """
    if plat in {"Linux", "Darwin"}:
        print(color(txt, "highlight", with_bgc or "ordinary", "red"), end='' if no_end else '\n')
    elif plat == "Windows":
        print(Fore.RED + Style.BRIGHT + win_back_color_map.get(with_bgc) or Back.RESET + txt, end='' if no_end else '\n')
    else:
        print(txt)


def color_it():
    dp = '    给文本上色的小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/basecolors'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("text", type=str, default='', help=f'{da}需要上色的文本')
    parser.add_argument("-a", "--show_all", type=str, dest="show_all", nargs='?', default='n',
                        help=f'{da}y/n 显示所有颜色，默认n')
    parser.add_argument("-ne", "--show_all_but_no_effect", type=str, dest="show_all_but_no_effect", nargs='?',
                        default='n',
                        help=f'{da}y/n 是否显示颜色代号，但不显示效果，默认n')
    parser.add_argument("-fc", "--front_color", type=str, dest="front_color", default='ordinary',
                        help=f'{da}字体颜色，默认ordinary')
    parser.add_argument("-bc", "--back_color", type=str, dest="back_color", default='ordinary',
                        help=f'{da}背景颜色，默认ordinary')
    parser.add_argument("-md", "--show_mode", type=str, dest="show_mode", default='ordinary',
                        help=f'{da}显示模式，默认ordinary')
    args = parser.parse_args()
    txt = args.text
    show_all_color = args.show_all
    no_effect = args.show_all_but_no_effect
    front_color = args.front_color
    back_color = args.back_color
    show_mode = args.show_mode

    show_all_color = True if show_all_color == 'y' or show_all_color is None else False
    effect = False if no_effect == 'y' or no_effect is None else True
    if show_all_color:
        show_all(effect)
    else:
        print()
        print_color(txt, show_mode=show_mode, back_color=back_color, front_color=front_color)
        print()


if __name__ == '__main__':
    show_all(False)
