import base64
import hashlib

import requests


class Notify(object):
    def __init__(self, host: str, key: str) -> None:
        self.s = requests.Session()
        self.key = key
        self.url = f"{host}/api/send"

    @classmethod
    def calculate_md5(cls, file_path: str) -> str:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as file:
            # 逐块读取文件并更新哈希值
            while chunk := file.read(8192):
                md5_hash.update(chunk)

        return md5_hash.digest().hex()

    @classmethod
    def encode_base64(cls, file_path: str) -> str:
        with open(file_path, "rb") as file:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
            return base64_encoded

    def send_text(self, msg: str) -> None:
        data = {
            "key": self.key,
            "data": {"msgtype": "text", "text": {"content": msg}},
        }
        self.s.post(self.url, json=data)

    def send_image(self, img_path: str) -> None:
        data = {
            "key": self.key,
            "data": {
                "msgtype": "image",
                "image": {
                    "base64": self.encode_base64(img_path),
                    "md5": self.calculate_md5(img_path),
                },
            },
        }
        self.s.post(self.url, json=data)

    def shop_refresh(self) -> None:
        self.send_text("商店刷新通知")
        self.send_image("output.jpg")
