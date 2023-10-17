import time
import os
from .utils.log import logger


class Buttons:
    """The button object containing the button string constants."""

    Y = "Y"
    X = "X"
    B = "B"
    A = "A"
    JCL_SR = "JCL_SR"
    JCL_SL = "JCL_SL"
    R = "R"
    ZR = "ZR"
    MINUS = "MINUS"
    PLUS = "PLUS"
    R_STICK_PRESS = "R_STICK_PRESS"
    L_STICK_PRESS = "L_STICK_PRESS"
    HOME = "HOME"
    CAPTURE = "CAPTURE"
    DPAD_DOWN = "DPAD_DOWN"
    DPAD_UP = "DPAD_UP"
    DPAD_RIGHT = "DPAD_RIGHT"
    DPAD_LEFT = "DPAD_LEFT"
    JCR_SR = "JCR_SR"
    JCR_SL = "JCR_SL"
    L = "L"
    ZL = "ZL"


class ProController:
    def __init__(self) -> None:
        import nxbt

        self.nx = nxbt.Nxbt()
        self.connect()

    def connect(self):
        import nxbt

        reconnect_addresses = self.nx.get_switch_addresses()
        self.controller_index = self.nx.create_controller(
            nxbt.PRO_CONTROLLER, reconnect_address=reconnect_addresses
        )
        self.nx.wait_for_connection(self.controller_index)
        time.sleep(1)
        logger.info("Connected switch.")
        self.press_buttons(Buttons.A)

    def disconnect(self):
        self.nx.remove_controller(self.controller_index)
        logger.info("Disconnected switch.")

    def press_buttons(self, button, down=0.1, up=0.1, block=True):
        buttons = []
        logger.info(f"Press button {button}")
        if isinstance(button, str):
            buttons.append(button)
        else:
            buttons = button
        self.nx.press_buttons(self.controller_index, buttons, down, up, block)

    def press_group(self, buttons, sleep=1):
        for b in buttons:
            self.press_buttons(b)
            if sleep:
                time.sleep(sleep)

    def press_button(self, button, sleep=2):
        """按下按键"""
        self.press_buttons(button)
        if sleep > 0:
            time.sleep(sleep)

    def press_a(self, sleep=3):
        self.press_button(Buttons.A, sleep)

    def press_b(self, sleep=2):
        self.press_button(Buttons.B, sleep)


debug = os.environ.get("A9_DEBUG", 0)
if debug:
    from unittest.mock import MagicMock

    pro = MagicMock()
    pro.press_buttons.return_value = None
    pro.press_group.return_value = None
    pro.press_button.return_value = None
    pro.press_a.return_value = None
    pro.press_b.return_value = None
else:
    pro = ProController()
