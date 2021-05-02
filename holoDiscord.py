import discord

import os
from os.path import join, dirname
from dotenv import load_dotenv


class holoDiscord:
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

TOKEN = -----------------------------------

CHANNEL_ID = --------------------------------

client = discord.Client() # 接続に使用するオブジェクト