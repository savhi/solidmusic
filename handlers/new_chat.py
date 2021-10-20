import asyncio

from pyrogram import filters
from pyrogram.types import ChatMemberUpdated, Message

from base.client_base import user, bot
from solidAPI.chat import add_chat, del_chat

from utils.functions import group_only


@bot.on_chat_member_updated(filters=filters.group)
async def on_bot_added(_, msg: ChatMemberUpdated):
    try:
        bot_id = (await bot.get_me()).id
        chat_id = msg.chat.id
        members_id = msg.new_chat_member.user.id
        lang = msg.new_chat_member.invited_by.language_code
        if members_id == bot_id:
            add_chat(chat_id, lang) if lang else "en"
    except AttributeError:
        pass


@bot.on_message(filters=filters.left_chat_member)
async def on_bot_kicked(_, msg: Message):
    try:
        bot_id = (await bot.get_me()).id
        chat_id = msg.chat.id
        members = msg.left_chat_member
        if members.id == bot_id:
            del_chat(chat_id)
            await user.send_message(chat_id, "bot left from chat, assistant left this chat too.")
            await asyncio.sleep(3)
            await user.leave_chat(chat_id)
            return
    except Exception as e:
        await msg.reply(f"{e}")


@bot.on_message(filters.command("addchat") & group_only)
async def add_chat_(_, message: Message):
    try:
        chat_id = message.chat.id
        lang = ""
        for members in message.chat.iter_members(1):
            lang += members.user.language_code
            return
        add_chat(chat_id, lang)
        await message.reply(f"{chat_id} added to our database")
    except Exception as e:
        await message.reply(f"{e}")


@bot.on_message(filters.command("delchat") & group_only)
async def del_chat_(_, message: Message):
    try:
        chat_id = int("".join(message.command[1]))
    except (KeyError, AttributeError):
        chat_id = message.chat.id
    try:
        del_chat(chat_id)
        await message.reply("chat deleted from db")
    except Exception as e:
        await message.reply(f"{e}")