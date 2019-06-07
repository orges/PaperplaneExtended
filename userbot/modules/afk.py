# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import random

from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, is_redis_alive)
from userbot.modules.dbhelper import is_afk, afk, afk_reason, no_afk
from userbot.events import register, errors_handler

# ========================= CONSTANTS ============================
AFKSTR = [
    "I'm busy right now. Please talk in a bag and when I come back you can just give me the bag!",
    "I'm away right now. If you need anything, leave a message after the beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "You missed me, next time aim better.",
    "I'll be back in a few minutes and if I'm not...,\nwait longer.",
    "I'm not here right now, so I'm probably somewhere else.",
    "Roses are red,\nViolets are blue,\nLeave me a message,\nAnd I'll get back to you.",
    "Sometimes the best things in life are worth waiting for…\nI'll be right back.",
    "I'll be right back,\nbut if I'm not right back,\nI'll be back later.",
    "If you haven't figured it out already,\nI'm not here.",
    "Hello, welcome to my away message, how may I ignore you today?",
    "I'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nWhere not even your messages can reach me!",
    "I'm away from the keyboard at the moment, but if you'll scream loud enough at your screen, I might just hear you.",
    "I went that way\n---->",
    "I went this way\n<----",
    "Please leave a message and make me feel even more important than I already am.",
    "I am not here so stop writing to me,\nor else you will find yourself with a screen full of your own messages.",
    "If I were here,\nI'd tell you where I am.\n\nBut I'm not,\nso ask me when I return...",
    "I am away!\nI don't know when I'll be back!\nHopefully a few minutes from now!",
    "I'm not available right now so please leave your name, number, and address and I will stalk you later.",
    "Sorry, I'm not here right now.\nFeel free to talk to my userbot as long as you like.\nI'll get back to you later.",
    "I bet you were expecting an away message!",
    "Life is so short, there are so many things to do...\nI'm away doing one of them..",
    "I am not here right now...\nbut if I was...\n\nwouldn't that be awesome?",
]
# =================================================================



@register(incoming=True, disable_edited=True)
@errors_handler
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    if not is_redis_alive():
        return
    AFK = await is_afk()
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if AFK is True:
            if mention.sender_id not in USERS:
                await mention.reply(
                    "Sorry! My boss is AFK due to "
                    + await afk_reason()
                    + ". Would ping him to look into the message soon😉"
                )
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % 5 == 0:
                    await mention.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + await afk_reason()
                        + "```"
                    )
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True)
@errors_handler
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    if not is_redis_alive():
        return
    AFK = await is_afk()
    if e.is_private and not (await e.get_sender()).bot:
        if AFK is True:
            if e.sender_id not in USERS:
                await e.reply(
                    "Sorry! My boss is AFK due to ```"
                    + await afk_reason()
                    + "``` I'll ping him to look into the message soon😉"
                )
                USERS.update({e.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif e.sender_id in USERS:
                if USERS[e.sender_id] % 5 == 0:
                    await e.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + await afk_reason()
                        + "```"
                    )
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk")
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    if not afk_e.text[0].isalpha() and afk_e.text[0] not in ("/", "#", "@",
                                                             "!"):
        message = afk_e.text
        string = str(message[5:])
        global ISAFK
        global AFKREASON
        await afk_e.edit("Alright, It's time to go AFK !!")
        if string != "":
            AFKREASON = string
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "You went AFK!")
        await afk(AFKREASON)
        raise StopPropagation


@register(outgoing=True)
@errors_handler
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if not is_redis_alive():
        return
    ISAFK = await is_afk()
    if ISAFK is True:
        await no_afk()
        x = await e.respond("I'm no longer AFK.")
        y = await e.respond(
            "`You recieved "
            + str(COUNT_MSG)
            + " messages while you were away. Check log for more details.`"
            + " `This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await x.delete()
        await y.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "Recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " chats while you weren't here",
            )
            for i in USERS:
                name = await e.client.get_entity(i)
                name0 = str(name.first_name)
                await e.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " sent you " + "`" + str(USERS[i]) + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


CMD_HELP.update({
    "afk":
    ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
