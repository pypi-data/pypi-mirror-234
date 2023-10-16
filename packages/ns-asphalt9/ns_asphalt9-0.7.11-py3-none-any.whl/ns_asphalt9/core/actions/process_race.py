import threading
import uuid
import time

from .. import consts, globals, ocr
from ..controller import Buttons, pro
from ..utils.log import logger
from ..utils.track_navi_data import get_navi_data
from .common import get_race_mode


def generate_random_filename():
    random_name = str(uuid.uuid4().hex)[:8]
    return random_name


def get_action(progress, navi_data, offset_progress):
    real_progress = round(progress + offset_progress)
    if navi_data:
        for p, a, d in navi_data:
            if p - real_progress in [-1, 0, 1]:
                return a, d
    return None, 0


def race_worker(progress_manager, navi_data, pro, race_navi_event):
    count = 0
    while race_navi_event.is_set():
        progress = progress_manager.get_progress()
        offset_progress = progress_manager.get_offset_progress()
        action, duration = get_action(progress, navi_data, offset_progress)
        if action:
            if action == "L":
                pro.press_buttons(Buttons.DPAD_LEFT)
            elif action == "R":
                pro.press_buttons(Buttons.DPAD_RIGHT)
            elif action == "LL":
                pro.press_buttons([Buttons.DPAD_LEFT, Buttons.DPAD_LEFT])
            elif action == "RR":
                pro.press_buttons([Buttons.DPAD_RIGHT, Buttons.DPAD_RIGHT])
            elif action == "B":
                pro.press_buttons(Buttons.B, duration)
            elif action == "BB":
                pro.press_buttons([Buttons.B, Buttons.B])
            elif action == "YY-1":
                pro.press_button(Buttons.Y, 0.7)
                pro.press_button(Buttons.Y, 0)
                count = 0
            elif action in ["YY-2", "YY-3"]:
                pro.press_buttons([Buttons.Y, Buttons.Y])
                count = 0
            else:
                logger.info(f"Action not support, action = {action}!")

        if count % 6 == 0:
            pro.press_button(Buttons.Y, 0.7)
            pro.press_button(Buttons.Y, 0)
        else:
            time.sleep(0.5)
        count += 1

    logger.info("Action woker quit.")


def start_race_worker(progress_manager, navi_data, pro, race_navi_event):
    t = threading.Thread(
        target=race_worker,
        args=(progress_manager, navi_data, pro, race_navi_event),
        daemon=True,
    )
    t.start()
    return t


class ProgessManager:
    fit_point_num = 2

    def __init__(self) -> None:
        self.history_progress = []
        self.start_time = time.time()
        self.offset_progress = 0

    def set_offset_progress(self, start_time, end_time, track_time):
        self.offset_progress = (end_time - start_time) * 100 / int(track_time)

    def get_offset_progress(self):
        return self.offset_progress

    def set_start_time(self):
        self.start_time = time.time()

    def put_progress(self, progress):
        if progress >= 0:
            duration = round(time.time() - self.start_time, 1)
            self.history_progress.append((duration, progress))

    def get_progress(self):
        fit_progress = self.get_fit_progress()
        logger.info(f"fit_progress = {fit_progress}")
        return fit_progress

    def get_fit_progress(self):
        if len(self.history_progress) >= self.fit_point_num:
            y = [p for _, p in self.history_progress[-self.fit_point_num :]]
            x = [t for t, _ in self.history_progress[-self.fit_point_num :]]
            # 计算拟合的斜率和截距
            n = self.fit_point_num
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            m = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / sum(
                (xi - mean_x) ** 2 for xi in x
            )
            b = mean_y - m * mean_x
            duration = round(time.time() - self.start_time, 1)
            fit_progress = int(duration * m + b)
            return fit_progress
        return -1


def process_race():
    logger.info("Start racing.")
    track = None
    progress = -1
    race_navi_event = threading.Event()
    mode = get_race_mode()
    enable_navi = globals.CONFIG[mode]["自动选路"]
    progress_manager = ProgessManager()
    logger.info(f"enable_navi = {enable_navi}")
    none_progress_count = 0
    for i in range(500):
        if 0 <= progress < 100:
            progress = ocr.OCR.get_progress(capture=True)
        else:
            page = ocr.OCR.get_page()
            progress = ocr.OCR.get_progress()
            if page.name == consts.loading_race:
                track = ocr.OCR.get_track()
                if track:
                    logger.info(f"Current track is {track['trackcn']}")
                navi_data = get_navi_data(track["tracken"]) if track else None
                if navi_data and enable_navi:
                    logger.info("Start aciton worker")
                    race_navi_event.set()
                    start_race_worker(progress_manager, navi_data, pro, race_navi_event)
                    break

            if page.name == consts.car_info:
                page.call_action()

            if page.name == consts.tickets:
                pro.press_group([Buttons.B] * 5, 3)
                break

            if ocr.OCR.has_next() or page.name in [
                consts.race_score,
                consts.race_results,
                consts.race_reward,
                consts.system_error,
                consts.connect_error,
                consts.no_connection,
                consts.multi_player,
                consts.error_code,
            ]:
                break
        pro.press_button(Buttons.Y, 0.7)
        pro.press_button(Buttons.Y, 0)

    if race_navi_event.is_set():
        progress_manager.set_start_time()
        for i in range(500):
            start_time = time.time()
            progress = ocr.OCR.get_progress(capture=True)
            end_time = time.time()
            progress_manager.set_offset_progress(start_time, end_time, track["time"])
            if progress < 0:
                none_progress_count += 1
            else:
                none_progress_count = 0
            logger.info(
                f"Current progress is {progress}, none_progress_count = {none_progress_count}"
            )
            if progress < 0 and ocr.OCR.has_next() or none_progress_count > 10:
                break
            progress_manager.put_progress(progress)
        race_navi_event.clear()
    globals.FINISHED_COUNT += 1
    logger.info(f"Already finished {globals.FINISHED_COUNT} times loop count = {i}.")
