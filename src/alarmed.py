#!/usr/bin/python

import argparse
import asyncio
from daemon import DaemonContext
from xdg import XDG_DATA_HOME, XDG_CONFIG_HOME
from datetime import datetime
from os import walk, replace, path
from subprocess import run
from time import sleep
from pathlib import Path

from Alarm import Alarm
from common import ALARM_DIR, PREVIOUS_ALARM_DIR, DEFAULT_ALARM_COMMAND, list_files

# TODO: Make this function modify global state in common.py
def init_data_folders(datadir=XDG_DATA_HOME, configdir=XDG_CONFIG_HOME):
  datadir.joinpath('alarmed/alarms').mkdir(parents=True, exist_ok=True)
  datadir.joinpath('alarmed/previous_alarms').mkdir(parents=True, exist_ok=True)
  configdir.joinpath('alarmed').mkdir(parents=True, exist_ok=True)

def is_finished(file):
  alarm = Alarm.readFromFile(path.join(ALARM_DIR, file))
  return alarm.timestamp <= datetime.now().timestamp()

async def execute_alarm_command(alarm):
  run(alarm.command or DEFAULT_ALARM_COMMAND.replace('%I', alarm.id).replace('%C', alarm.comment or ''), shell=True)

def move_finished_alarm(alarm_file, finished_alarm_dir=PREVIOUS_ALARM_DIR):
  replace(
    path.join(ALARM_DIR, alarm_file),
    path.join(finished_alarm_dir, alarm_file)
  )

async def execute_finished_alarms():
  files = list_files(ALARM_DIR)

  if files == []:
    return

  finished_alarms = [file for file in files if is_finished(file)]

  for file in finished_alarms:
    alarm = Alarm.readFromFile(path.join(ALARM_DIR, file))
    print(f'[{datetime.now().strftime("%H:%M")}] Executing alarm with ID {alarm.id}')
    move_finished_alarm(file)
    asyncio.create_task(execute_alarm_command(alarm))

async def alarm_check_loop():
  while True:
    await execute_finished_alarms()
    sleep(1)

async def main():
  # with DaemonContext():
  init_data_folders()
  await alarm_check_loop()

if __name__ == '__main__':
  asyncio.run(main())