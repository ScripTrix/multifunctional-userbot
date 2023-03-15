from pyrogram import Client, filters
from pyrogram import enums
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta
import os
from time import time
from time import sleep
import random
from replacement_map import REPLACEMENT_MAP
from random import shuffle
from apscheduler.schedulers.background import BackgroundScheduler
import keep_alive

texnic_file = "texnic.mp4"

spot_bot_id = 5633724545

app = Client("my_account",
             api_id=os.environ.get("api_id"),
             api_hash=os.environ.get("api_hash"))


# Получение карточек каждые 4 часа
def get_card():
  app.send_message(spot_bot_id, text="🧀 Получить карту")
  pass


scheduler = BackgroundScheduler()
scheduler.add_job(get_card, "interval", hours=4)


# Промокоды для SPOT
@app.on_message(
  filters.command("promo", prefixes="/") & (~filters.chat(spot_bot_id)))
def promo(_, msg):
  try:
    app.send_message(chat_id=spot_bot_id, text=msg.text)
  except FloodWait as e:
    sleep(e.x)


# Эффект печатания
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
  origin_text = msg.text.split(".type ", maxsplit=1)[1]
  text = origin_text
  tbp = ""  # to be printed
  typing_symbol = "▒"

  while (tbp != origin_text):
    try:
      msg.edit(tbp + typing_symbol)
      sleep(0.1)  # 100 ms

      tbp = tbp + text[0]
      text = text[1:]

      msg.edit(tbp)
      sleep(0.1)

    except FloodWait as e:
      sleep(e.x)


# Эффект процесса
@app.on_message(filters.command("hack", prefixes=".") & filters.me)
def hack(_, msg):
  perc = 0
  origin_text = msg.text.replace(".hack ", "")

  while (perc <= 99):
    try:
      text = f"👽 {origin_text} ..." + str(perc) + "%"
      msg.edit(text)

      perc += random.randint(1, 3)

    except FloodWait as e:
      sleep(e.x)

  if (perc == 100):
    msg.edit("Всё прошло успешно! 🥷")
  else:
    msg.edit("Накрыли лавочку! 🥴")


# Перевернутое сообщение (только латиница)
@app.on_message(filters.command("flip", prefixes=".") & filters.me)
def flip(_, msg):
  text = msg.text.split(".flip ", maxsplit=1)[1]
  final_str = ""
  for char in text:
    if char in REPLACEMENT_MAP.keys():
      new_char = REPLACEMENT_MAP[char]
    else:
      new_char = char
    final_str += new_char
  if text != final_str:
    msg.edit(final_str)
  else:
    msg.edit(text)


# Паша Техник заливает перцем
@app.on_message(filters.command("texnic", prefixes=".") & filters.me)
def texnic(_, msg):
  chat_id = msg.chat.id
  msg.edit("Пашок залил пацанов перцем, придётся отмываться. 🌶")
  app.send_animation(chat_id, animation=texnic_file, unsave=True)
  members = [
    x for x in app.get_chat_members(chat_id)
    if x.status not in (enums.ChatMemberStatus.ADMINISTRATOR,
                        enums.ChatMemberStatus.OWNER,
                        enums.ChatMemberStatus.RESTRICTED)
  ]
  shuffle(members)

  for i in range(len(members) // 2):
    try:
      app.restrict_chat_member(
        chat_id=chat_id,
        user_id=members[i].user.id,
        permissions=ChatPermissions(),
        until_date=datetime.now() + timedelta(days=1),
      )

      print("muted", members[i].user.username)
      app.send_message(chat_id=chat_id,
                       text=f"@{members[i].user.username} пустил слёзы. 💦")
    except FloodWait as e:
      print("> waiting", e.x, "seconds.")
      time.sleep(e.x)


# Информация о чате
@app.on_message(filters.command("info", prefixes=".") & filters.me)
def info(_, msg):
  print(msg)


scheduler.start()
keep_alive.keep_alive()
app.run()
