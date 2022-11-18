'''
Declare variables used in bot.
This file is a based on the variables.py file from my other bot.
'''
import json
from typing import List
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands

#v[major].[minor].[release].[build]
VERSION = "v0.0.1.0"


intents = discord.Intents.default()
handler = RotatingFileHandler(filename='discord.log',
                            encoding='utf-8',
                            mode='w',
                            backupCount=10,
                            maxBytes=100000)

class Secret:
    '''Class for secret.json management'''
    def __init__(self) -> None:
        self._file = 'secret.json'
        with open(self._file,encoding="utf-8",mode='r') as secret_f:
            self.secret = json.load(secret_f)
        self.token = self.secret['token']

    def __repr__(self) -> str:
        return "[OBFUSCATED]"

    def __str__(self) -> str:
        return "[OBFUSCATED]"



class Config: #Note: Currently config is global, but I plan to make it per server.
    '''Class for convinient config access'''
    def __init__(self,bot: commands.Bot) -> None:
        self._file = 'config.json'
        with open(self._file,encoding="utf-8",mode='r') as config_f:
            self._config = json.load(config_f)
        self._bt = bot

    def __dict__(self) -> dict:
        return self._config

    def update(self) -> None:
        '''Update the config.json file to reflect changes'''
        with open(self._file,encoding="utf-8",mode='w') as config_f:
            json.dump(self._config,config_f,indent=4)
            config_f.truncate()

    @property
    def guild(self) -> discord.Guild:
        '''Returns the guild object'''
        gld = self._bt.get_guild(self._config['guild_id'])
        if isinstance(gld, discord.Guild):
            return gld
        raise ValueError("Guild Not Found")

    @guild.setter
    def guild(self, value: discord.Guild) -> None:
        '''Sets the guild object'''
        self._config['guild_id'] = value.id
        self.update()

    @property
    def ticket_users(self) -> List[int]:
        '''List of users who are tracked for ticket creation'''
        return self._config['ticket_users']

    @ticket_users.setter
    def ticket_users(self, value: List[int]) -> None:
        '''Sets the list of users who are tracked for ticket creation'''
        self._config['ticket_users'] = value
        self.update()

    @property
    def staff(self) -> List[discord.Role]:
        '''List of users who are staff'''
        staff = []
        for role in self._config['staff']:
            stf_role = self.guild.get_role(role)
            if isinstance(stf_role, discord.Role):
                staff.append(stf_role)
        return staff

    @staff.setter
    def staff(self, value: List[discord.Role]) -> None:
        '''Sets the list of users who are staff'''
        self._config['staff'] = [role.id for role in value]
        self.update()
        