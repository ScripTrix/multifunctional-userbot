import os
import random
import keep_alive
from time import time
from time import sleep
from pyrogram import enums
from random import shuffle
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions
from apscheduler.schedulers.background import BackgroundScheduler

texnic_file = "texnic.mp4"

spot_bot_id = 5633724545
spot_schedule_id = 'spot_schedule_id'

app = Client("my_account",
             api_id=os.environ.get("api_id"),
             api_hash=os.environ.get("api_hash"))


# Получение карточки
def get_card():
  app.send_message(spot_bot_id, text="🧀 Получить карту")
  print(f"[{datetime.now()}] ---> [Сard request]")


# Планировщик
scheduler = BackgroundScheduler(timezone="UTC", )


# Инициализация планировщика
def init_schedule():

  if(scheduler.get_job(spot_schedule_id)):
    scheduler.remove_job(spot_schedule_id)
    print(f"[{datetime.now()}] ---> [Schedule removed]")
  scheduler.add_job(get_card, trigger="interval", 
                    hours=4, seconds=5, id=spot_schedule_id)
  print(f"[{datetime.now()}] ---> [Schedule initialized]")


# Обновить планировщик
@app.on_message(filters.command("update", prefixes=".") & filters.me)
def scheduler_update(_, msg):
  try:
    get_card()
    init_schedule()
  except FloodWait as e:
    sleep(e.x)


# Перехват и отправка промокодов в SPOT
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


# Инициализация приложения
def initialize():
  print(f"[{datetime.now()}] ---> [Initialization]")
  init_schedule()
  print(f"[{datetime.now()}] ---> [Startup]")
  scheduler.start()
  keep_alive.keep_alive()
  print(f"[{datetime.now()}] ---> [Application started successfully]")
  app.run()


initialize()
