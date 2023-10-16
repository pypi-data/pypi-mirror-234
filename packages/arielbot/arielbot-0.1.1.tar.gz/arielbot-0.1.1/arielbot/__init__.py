import click
import json
from os import path, getcwd, mkdir
import dotenv
import nonebot
from .bot import app

# env = {
#     'DRIVER':'~aiohttp',
#     'SUPERUSERS': [],
#     'DynTextFont': '',
#     'DynEmojiFont': '',
#     'DynFontStyle': ''

# }


@click.group()
def main():
    pass


@click.command()
def run():
    create_plugins_dir()
    nonebot.run(app=app)


main.add_command(run)





def create_plugins_dir():
    plugins_dir_path = path.join(getcwd(), "plugins")
    if not path.exists(plugins_dir_path):
        mkdir(plugins_dir_path)
