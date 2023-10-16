import time
from ..controller import pro, Buttons
from .. import globals, consts


def connect():
    """连接手柄"""
    pro.connect()


def disconnect():
    """断开手柄"""
    pro.disconnect()


def connect_controller():
    """连接手柄"""
    pro.press_buttons([Buttons.L, Buttons.R], down=1)
    time.sleep(1)
    pro.press_buttons([Buttons.A], down=0.5)


def restart(page=None):
    """重启游戏"""
    # 回到主页
    pro.press_button(Buttons.HOME, 3)
    # 关闭
    pro.press_button(Buttons.X, 1)
    # 按一下确认关闭，再打开
    pro.press_group([Buttons.A] * 3, 2)


def demoted():
    """降级"""
    pro.press_button(Buttons.B, 3)


def promoted():
    """升级"""
    pro.press_button(Buttons.A, 3)


def set_eng():
    pass


def system_error():
    pro.press_group([Buttons.A] * 3, 3)


def loading_game():
    pass


def get_race_mode():
    mode = globals.MODE if globals.MODE else globals.CONFIG["模式"]
    if mode in [consts.mp_zh, consts.mp1_zh]:
        if globals.CONFIG["模式"] == consts.mp3_zh:
            return consts.mp3_zh
        elif globals.CONFIG["模式"] == consts.mp2_zh:
            return consts.mp2_zh
        else:
            return consts.mp1_zh
    else:
        return mode
