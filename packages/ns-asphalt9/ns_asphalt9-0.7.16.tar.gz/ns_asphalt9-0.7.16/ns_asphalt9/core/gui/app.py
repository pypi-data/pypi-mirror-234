import json
import os
import tkinter

import customtkinter
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self, queue, config_name):
        super().__init__()

        self.title("A9 AUTO")
        self.geometry("700x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._init_data(queue, config_name)

        # load images with light and dark mode image
        self._load_image()

        # create navigation frame
        self._build_navi()

        # create home frame
        self._build_home()

        # create settings frame
        self._build_settings()

        self._build_reward()

        # create third frame
        self.help = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        # select default frame
        self.select_frame_by_name("home")
        self.save_settings()

    def _init_data(self, queue, config_name):
        self.queue = queue
        self.settings_data = None
        self.config_file = f"{config_name}.json"
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                self.settings_data = json.load(file)

    def _load_image(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "logo.png")),
            size=(26, 26),
        )
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home.png")),
            size=(20, 20),
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "settings.png")),
            size=(20, 20),
        )
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "help.png")),
            size=(20, 20),
        )
        self.reward_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "reward.png")),
            size=(20, 20),
        )
        self.reward_wechat_qrcode = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "reward_qrcode.jpeg")),
            size=(300, 300),
        )

    def _build_navi(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  A9 Auto",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="开始",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="配置",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.settings_button_event,
        )
        self.settings_button.grid(row=2, column=0, sticky="ew")

        self.reward_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="打赏",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.reward_image,
            anchor="w",
            command=self.reward_button_event,
        )
        self.reward_button.grid(row=3, column=0, sticky="ew")

        self.help_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="帮助",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image,
            anchor="w",
            command=self.help_button_event,
        )
        self.help_button.grid(row=4, column=0, sticky="ew")

    def _build_home(self):
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=250, height=460)
        self.textbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.entry = customtkinter.CTkEntry(
            self.home_frame, placeholder_text="Please input command."
        )
        self.entry.bind("<Return>", self.on_entry_enter)
        self.entry.grid(
            row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew"
        )

    def _build_reward(self):
        self.reward = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.reward.grid_columnconfigure(0, weight=1)

        reward_image = customtkinter.CTkButton(
            self.reward,
            image=self.reward_wechat_qrcode,
            text="",
            fg_color="white",
            # text_color="transparent",
            hover_color=("white", "white"),
        )
        reward_image.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")

        reward_text = customtkinter.CTkLabel(
            self.reward,
            text="因为你的支持，A9 Auto才能一直保持更新，\n适配NS A9的页面修改，增加更多自动功能。",
            fg_color="transparent",
        )

        reward_text.grid(row=1, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

        # self.textbox = customtkinter.CTkTextbox(self.home_frame, width=250, height=460)
        # self.textbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # self.entry = customtkinter.CTkEntry(
        #     self.home_frame, placeholder_text="Please input command."
        # )
        # self.entry.bind("<Return>", self.on_entry_enter)
        # self.entry.grid(
        #     row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew"
        # )

    def _build_settings(self):
        """配置页"""
        self.setting_modules = {}
        self.settings = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        for row, label_text in enumerate(
            ["模式", "任务", "多一", "多二", "寻车", "传奇寻车", "多三", "大奖赛", "通知", "野兽年"]
        ):
            label = customtkinter.CTkLabel(master=self.settings, text=f"{label_text}:")
            label.grid(
                row=row,
                column=0,
                columnspan=1,
                padx=10,
                pady=(20 if row == 0 else 10, 10),
                sticky="",
            )

        # 模式配置
        self._build_mode()
        # 任务配置
        self._build_tasks()
        # 多人一配置
        self._build_mp1()
        # 多人二配置
        self._build_common(row=3, key="多人二", add_reset_type=True)
        # 寻车配置
        self._build_common(
            row=4, key="寻车", add_event_type=True, add_event_position=True
        )
        # 传奇寻车配置
        self._build_common(row=5, key="传奇寻车", add_event_position=True)
        # 多人三配置
        self._build_common(row=6, key="多人三")
        # 大奖赛配置
        self._build_prix(row=7)
        # 通知配置
        self._build_notify(row=8)
        # 野兽年
        self._build_common(row=9, key="野兽年", add_event_position=True)

    def _build_mode(self):
        """模式设置选项"""
        self.mode = tkinter.StringVar()
        self.mode_buttons = customtkinter.CTkSegmentedButton(
            self.settings,
            variable=self.mode,
            command=self.save_settings,
            values=["多人一", "多人二", "多人三", "野兽年"],
        )
        self.mode_buttons.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="ew"
        )
        if self.settings_data:
            self.mode_buttons.set(self.settings_data["模式"])
        self.setting_modules["模式"] = self.mode_buttons

    def _build_navi_box(self, frame, key):
        """自动选路选项"""
        navi_label = customtkinter.CTkLabel(master=frame, text="自动选路:")
        navi_label.grid(row=0, column=0, padx=10, pady=(10, 10))

        enable_navi = customtkinter.CTkCheckBox(
            master=frame, text="是否开启", command=self.save_settings
        )
        enable_navi.grid(row=0, column=1, pady=(10, 10), padx=(20, 0), sticky="ew")

        self.setting_modules[key]["自动选路"] = enable_navi

        if (
            self.settings_data
            and key in self.settings_data
            and "自动选路" in self.settings_data[key]
        ):
            if self.settings_data[key]["自动选路"]:
                enable_navi.select()

    def _build_mp1(self):
        """多人一配置"""
        mp1_frame = customtkinter.CTkFrame(self.settings, width=340)
        mp1_frame.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.setting_modules["多人一"] = {}

        self._build_navi_box(mp1_frame, "多人一")

        self.tabview = customtkinter.CTkTabview(mp1_frame, width=340)
        self.tabview.grid(
            row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        tabs = ["青铜", "白银", "黄金", "铂金"]
        for tab_index, tab_name in enumerate(tabs):
            self.setting_modules["多人一"][tab_name] = {}
            self.tabview.add(tab_name)

            car_level = customtkinter.CTkLabel(
                master=self.tabview.tab(tab_name), text="车库等级:"
            )
            car_level.grid(row=1, column=0, padx=10, pady=(10, 10))
            option_level = customtkinter.CTkOptionMenu(
                self.tabview.tab(tab_name),
                dynamic_resizing=False,
                values=tabs[: tab_index + 1],
                width=100,
                height=28,
                command=self.save_settings,
            )
            option_level.grid(row=1, column=1, padx=10, pady=(10, 10))

            if self.settings_data:
                option_level.set(self.settings_data["多人一"][tab_name]["车库等级"])

            self.setting_modules["多人一"][tab_name]["车库等级"] = option_level

            self._build_car_position(
                self.tabview.tab(tab_name),
                self.setting_modules["多人一"][tab_name],
                self.settings_data["多人一"][tab_name] if self.settings_data else {},
                2,
            )

    def _build_tasks(self):
        """任务配置"""
        tasks_frame = customtkinter.CTkFrame(self.settings, width=340)
        tasks_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        tasks = [
            ("免费抽卡", ["180", "240"]),
            ("大奖赛抽卡", ["240"]),
            ("寻车", ["130"]),
            ("传奇寻车", ["100"]),
            ("重启", ["60"]),
            ("商店通知", []),
        ]
        self.setting_modules["任务"] = []
        for row, (task, values) in enumerate(tasks):
            task_box = customtkinter.CTkCheckBox(
                master=tasks_frame, text=task, command=self.save_settings
            )
            task_box.grid(row=row, column=1, pady=(10, 10), padx=(20, 0), sticky="ew")

            if values:
                task_combobox = customtkinter.CTkComboBox(
                    tasks_frame, values=values, width=100, command=self.save_settings
                )
                task_combobox.grid(row=row, column=2, padx=(20, 100), pady=(10, 10))
            else:
                task_combobox = {}

            if self.settings_data and row < len(self.settings_data["任务"]):
                if self.settings_data["任务"][row]["运行"]:
                    task_box.select()
                if values:
                    task_combobox.set(self.settings_data["任务"][row]["间隔"])

            self.setting_modules["任务"].append(
                {"名称": task, "运行": task_box, "间隔": task_combobox}
            )

    def _build_common(
        self,
        row=6,
        key="多人三",
        add_event_position=False,
        add_reset_type=False,
        add_event_type=False,
    ):
        """多人和寻车配置"""
        self.setting_modules[key] = {}
        frame = customtkinter.CTkFrame(self.settings, width=340)
        frame.grid(
            row=row, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self._build_navi_box(frame, key)
        base_row = 1
        if add_event_position:
            car_hunt_position = customtkinter.CTkLabel(master=frame, text="位置:")
            car_hunt_position.grid(row=1, column=0, padx=(15, 10), pady=(10, 10))
            position_option = customtkinter.CTkOptionMenu(
                frame,
                dynamic_resizing=False,
                values=[str(i) for i in range(0, 20)],
                width=100,
                height=28,
                command=self.save_settings,
            )

            position_option.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

            if (
                self.settings_data
                and key in self.settings_data
                and "位置" in self.settings_data[key]
            ):
                position_option.set(self.settings_data[key]["位置"])
            self.setting_modules[key]["位置"] = position_option
            base_row += 1

        if add_reset_type:
            reset_type_label = customtkinter.CTkLabel(master=frame, text="复位:")
            reset_type_label.grid(row=base_row, column=0, padx=(15, 10), pady=(10, 10))
            reset_type_option = customtkinter.CTkOptionMenu(
                frame,
                dynamic_resizing=False,
                values=[str(i) for i in range(0, 2)],
                width=100,
                height=28,
                command=self.save_settings,
            )

            reset_type_option.grid(row=base_row, column=1, padx=(10, 10), pady=(10, 10))

            if (
                self.settings_data
                and key in self.settings_data
                and "复位" in self.settings_data[key]
            ):
                reset_type_option.set(self.settings_data[key]["复位"])
            self.setting_modules[key]["复位"] = reset_type_option
            base_row += 1

        if add_event_type:
            event_type_label = customtkinter.CTkLabel(master=frame, text="活动:")
            event_type_label.grid(row=base_row, column=0, padx=(15, 10), pady=(10, 10))
            event_type_option = customtkinter.CTkOptionMenu(
                frame,
                dynamic_resizing=False,
                values=["每日", "特殊"],
                width=100,
                height=28,
                command=self.save_settings,
            )

            event_type_option.grid(row=base_row, column=1, padx=(10, 10), pady=(10, 10))

            if (
                self.settings_data
                and key in self.settings_data
                and "活动" in self.settings_data[key]
            ):
                event_type_option.set(self.settings_data[key]["活动"])
            self.setting_modules[key]["活动"] = event_type_option
            base_row += 1

        self._build_car_position(
            frame,
            self.setting_modules[key],
            self.settings_data[key]
            if self.settings_data and key in self.settings_data
            else {},
            base_row,
        )
        return frame

    def _build_prix(self, row=7):
        """大奖赛配置项"""
        self.setting_modules["大奖赛"] = {}
        prix_setting_frame = customtkinter.CTkFrame(self.settings, width=340)
        prix_setting_frame.grid(
            row=7, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        prix_position = customtkinter.CTkLabel(master=prix_setting_frame, text="位置:")
        prix_position.grid(row=1, column=0, padx=(15, 10), pady=(10, 10))
        prix_position_option = customtkinter.CTkOptionMenu(
            prix_setting_frame,
            dynamic_resizing=False,
            values=[str(i) for i in range(0, 10)],
            width=100,
            height=28,
            command=self.save_settings,
        )

        prix_position_option.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))
        if self.settings_data and "大奖赛" in self.settings_data:
            prix_position_option.set(self.settings_data["大奖赛"]["位置"])
        self.setting_modules["大奖赛"]["位置"] = prix_position_option

    def _build_notify(self, row=7):
        """通知配置项"""
        self.setting_modules["通知"] = {}
        notify_setting_frame = customtkinter.CTkFrame(self.settings, width=340)
        notify_setting_frame.grid(
            row=8, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        host_label = customtkinter.CTkLabel(master=notify_setting_frame, text="Host:")
        host_label.grid(row=1, column=0, padx=(15, 10), pady=(10, 10))
        host_input = customtkinter.CTkEntry(
            master=notify_setting_frame,
            width=200,
            height=28,
        )
        host_input.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

        host_input.bind("<KeyRelease>", self.save_settings)
        key_label = customtkinter.CTkLabel(master=notify_setting_frame, text="Key:")
        key_label.grid(row=2, column=0, padx=(15, 10), pady=(10, 10))
        key_input = customtkinter.CTkEntry(
            master=notify_setting_frame, width=200, height=28
        )
        key_input.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))
        key_input.bind("<KeyRelease>", self.save_settings)

        if self.settings_data and "通知" in self.settings_data:
            host_input.insert(0, self.settings_data["通知"]["Host"])
            key_input.insert(0, self.settings_data["通知"]["Key"])

        self.setting_modules["通知"]["Host"] = host_input
        self.setting_modules["通知"]["Key"] = key_input

    def _build_car_position(self, frame, module_container, data_container, base_row):
        """车库位置配置"""
        car_position = customtkinter.CTkLabel(master=frame, text="车库位置:")
        car_position.grid(row=base_row, column=0, padx=(15, 10), pady=(10, 10))
        row = customtkinter.CTkLabel(master=frame, text="row")
        row.grid(row=base_row, column=1, padx=(0, 0), pady=(10, 10), sticky="nsew")
        col = customtkinter.CTkLabel(master=frame, text="col")
        col.grid(row=base_row, column=2, padx=(0, 10), pady=(10, 10), sticky="nsew")
        module_container["车库位置"] = []

        for r in range(6):
            option1 = customtkinter.CTkOptionMenu(
                frame,
                dynamic_resizing=False,
                values=[str(i) for i in range(0, 3)],
                width=100,
                height=28,
                command=self.save_settings,
            )

            option2 = customtkinter.CTkOptionMenu(
                frame,
                dynamic_resizing=False,
                values=[str(i) for i in range(0, 30)],
                width=100,
                height=28,
                command=self.save_settings,
            )

            option1.grid(row=r + base_row + 1, column=1, padx=(10, 10), pady=(10, 10))
            option2.grid(row=r + base_row + 1, column=2, padx=(10, 10), pady=(10, 10))

            if self.settings_data and data_container:
                option1.set(data_container["车库位置"][r]["row"])
                option2.set(data_container["车库位置"][r]["col"])

            module_container["车库位置"].append({"row": option1, "col": option2})

    def show(self, text):
        self.textbox.insert(tkinter.END, text + "\n")
        self.textbox.see(tkinter.END)

    def on_entry_enter(self, *args):
        text = self.entry.get()
        self.queue.put(text)
        self.entry.delete(0, tkinter.END)

    def save_settings(self, *args, **kwargs):
        def get_value(objs):
            if isinstance(objs, dict):
                res = {}
                for obj in objs:
                    res[obj] = get_value(objs[obj])
                return res
            elif isinstance(objs, list):
                res = []
                for obj in objs:
                    res.append(get_value(obj))
                return res
            elif isinstance(objs, str):
                return objs
            else:
                return objs.get()

        def convert_dict_values(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == "车库位置":
                        data[key] = [
                            v for v in value if int(v["col"]) and int(v["row"])
                        ]
                    if isinstance(value, str) and value.isdigit():
                        data[key] = int(value)
                    if isinstance(value, (dict, list)):
                        convert_dict_values(value)  # 递归调用
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, str) and item.isdigit():
                        data[i] = int(item)
                    elif isinstance(item, (dict, list)):
                        convert_dict_values(item)  # 递归调用

        res = get_value(self.setting_modules)
        self.settings_data = res
        with open(self.config_file, "w") as file:
            file.write(json.dumps(res, indent=2, ensure_ascii=False))
        convert_dict_values(res)
        self.queue.put(res)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.settings_button.configure(
            fg_color=("gray75", "gray25") if name == "settings" else "transparent"
        )
        self.help_button.configure(
            fg_color=("gray75", "gray25") if name == "help" else "transparent"
        )

        self.reward_button.configure(
            fg_color=("gray75", "gray25") if name == "reward" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.settings.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings.grid_forget()
        if name == "help":
            self.help.grid(row=0, column=1, sticky="nsew")
        else:
            self.help.grid_forget()
        if name == "reward":
            self.reward.grid(row=0, column=1, sticky="nsew")
        else:
            self.reward.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def help_button_event(self):
        self.select_frame_by_name("help")

    def reward_button_event(self):
        self.select_frame_by_name("reward")


if __name__ == "__main__":
    app = App()
    app.mainloop()
