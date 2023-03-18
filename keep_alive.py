from flask import Flask
from threading import Thread
from datetime import datetime

flask = Flask('app')


@flask.route('/')
def main():
  return "Bot successfully started!"


def run():
  flask.run(host="0.0.0.0", port=8080)


def keep_alive():
  server = Thread(target=run)
  server.start()
  print(f"[{datetime.now()}] ---> [Flask server initialized]")
