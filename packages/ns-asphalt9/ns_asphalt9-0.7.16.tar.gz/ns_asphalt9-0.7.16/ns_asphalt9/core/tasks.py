import threading
import traceback
from datetime import datetime

from . import actions, consts, globals
from .cache import cache
from .utils.decorator import cache_decorator
from .utils.log import logger


class Task:
    name = None
    action = None
    page = None
    # 是否自动返回模式设置的任务中
    auto_done = False

    def __init__(self, page, last_task) -> None:
        self.page = page
        self.last_task = last_task

    def process(self):
        logger.debug(f"Call aciton func = {self.action}")
        try:
            self.action(self.page)
        except Exception as err:
            logger.error(
                f"Caught exception, err = {err}, traceback = {traceback.format_exc()}"
            )
        if self.auto_done:
            TaskManager.set_done()
            if self.last_task:
                globals.task_queue.put(self.last_task)


@cache_decorator("task")
class Mp1Task(Task):
    """多人一任务"""

    name = consts.mp1_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class Mp2Task(Task):
    """多人二任务"""

    name = consts.mp2_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class Mp3Task(Task):
    """多人三任务"""

    name = consts.mp3_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class CarHuntTask(Task):
    """寻车任务"""

    name = consts.car_hunt_zh
    action = staticmethod(actions.enter_carhunt)


@cache_decorator("task")
class LegendaryHuntTask(Task):
    """传奇寻车任务"""

    name = consts.legendary_hunt_zh
    action = staticmethod(actions.enter_legend_carhunt)


@cache_decorator("task")
class BeastYearTask(Task):
    """野兽年任务"""

    name = consts.beast_year_zh
    action = staticmethod(actions.enter_beast_year)


@cache_decorator("task")
class FreePackTask(Task):
    """免费抽卡任务"""

    name = consts.free_pack_zh
    action = staticmethod(actions.free_pack)
    auto_done = True


@cache_decorator("task")
class PrixPackTask(Task):
    """大奖赛抽卡任务"""

    name = consts.prix_pack_zh
    action = staticmethod(actions.prix_pack)
    auto_done = True


@cache_decorator("task")
class RestartTask(Task):
    """重启任务"""

    name = consts.restart
    action = staticmethod(actions.restart)
    auto_done = True


@cache_decorator("task")
class ShopNotifyTask(Task):
    """商店通知任务"""

    name = consts.shop_notify
    action = staticmethod(actions.shop_notify)
    auto_done = True


class TaskManager:
    timers = []
    current_task = ""
    last_task = ""
    status = consts.TaskStatus.default

    @classmethod
    def task_init(cls):
        if "任务" not in globals.CONFIG:
            return
        car_hunt_task = None
        for task in globals.CONFIG["任务"]:
            if task["运行"] > 0 and task["间隔"]:
                cls.task_producer(task["名称"], task["间隔"])
                if task["名称"] in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
                    car_hunt_task = task["名称"]
        if car_hunt_task:
            globals.task_queue.put(car_hunt_task)

    @classmethod
    def task_producer(cls, task, duration, skiped=False):
        if skiped:
            globals.task_queue.put(task)
        else:
            logger.info(f"Start task {task} producer, duration = {duration}min")
            skiped = True
        timer = threading.Timer(
            duration * 60, cls.task_producer, (task, duration), {"skiped": skiped}
        )
        timer.start()
        cls.timers.append(timer)

    @classmethod
    def destroy(cls):
        for t in cls.timers:
            t.cancel()

    @classmethod
    def task_dispatch(cls, page) -> bool:
        ShopNotifyProducer.run()
        if page.name in consts.TASK_DISPATCH_PAGES:
            # 没有任务并且是已完成状态
            if globals.task_queue.empty() and cls.status == consts.TaskStatus.done:
                cls.task_enter(globals.CONFIG["模式"], page=page)
                cls.status = consts.TaskStatus.default
                return True
            # 有任务去队列取任务
            if not globals.task_queue.empty():
                task = globals.task_queue.get()
                logger.info(f"Get {task} task from queue.")
                cls.status = consts.TaskStatus.start
                cls.last_task = cls.current_task
                cls.current_task = task
                cls.task_enter(task, page)
                return True
        return False

    @classmethod
    def task_enter(cls, task_name, page) -> None:
        logger.info(f"Start process {task_name} task.")
        task_cls = cache.get_by_type("task", task_name)
        task_instance: Task = task_cls(page, cls.last_task)
        task_instance.process()

    @classmethod
    def set_done(cls) -> None:
        if cls.status == consts.TaskStatus.start:
            cls.status = consts.TaskStatus.done
            cls.current_task = ""


class ShopNotifyProducer:
    notify_list = []

    @classmethod
    def shop_notify_status(cls) -> bool:
        for task in globals.CONFIG["任务"]:
            if task["名称"] == "商店通知" and task["运行"] > 0:
                return True
        return False

    @classmethod
    def run(cls) -> None:
        if "通知" not in globals.CONFIG or not cls.shop_notify_status():
            return
        now_utc = datetime.utcnow()
        # 北京时间17点，20点, 凌晨2点
        if now_utc.hour in [9, 12, 18] and now_utc.minute < 10:
            notify_key = f"{now_utc.month}_{now_utc.day}_{now_utc.hour}"
            if notify_key not in cls.notify_list:
                cls.notify_list.append(notify_key)
                globals.task_queue.put(consts.shop_notify)
