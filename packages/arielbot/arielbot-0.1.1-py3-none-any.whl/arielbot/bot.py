import nonebot
from nonebot.adapters.red import Adapter as RedAdapter
from os import path, getcwd, listdir
import sys
import dotenv

import json

env = {
    'DRIVER':'~aiohttp',
    'SUPERUSERS': [],
    'DynTextFont': '',
    'DynEmojiFont': '',
    'DynFontStyle': ''

}


def create_config():
    env_file_path = path.join(getcwd(), ".env.prod")
    if not path.exists(env_file_path):
        red_bots= [{"port": "16530","token": "xxx","host": "localhost"}]
        token = input("请输入token：")
        print(red_bots[0])
        red_bots[0]["token"] = token
        for key, value in env.items():
            dotenv.set_key(
                env_file_path,
                key,
                str(value).replace(' ', ''),
                quote_mode="never")
        dotenv.set_key(env_file_path,"RED_BOTS",json.dumps(red_bots),quote_mode='never')

create_config()

sys.path.append(path.join(getcwd(), "plugins"))

nonebot.init()
nonebot.load_plugin("arielbot.plugins.Core")
nonebot.load_all_plugins([i for i in listdir(path.join(getcwd(), "plugins"))], [])
driver = nonebot.get_driver()
driver.register_adapter(RedAdapter)
app = nonebot.get_asgi()
config = nonebot.get_driver().config

