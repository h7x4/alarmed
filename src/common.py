from pathlib import Path
from xdg import XDG_DATA_HOME, XDG_CONFIG_HOME
from os import walk

ALARM_DIR = XDG_DATA_HOME.joinpath('alarmed/alarms').absolute()
PREVIOUS_ALARM_DIR = XDG_DATA_HOME.joinpath('alarmed/previous_alarms').absolute()
DEFAULT_ALARM_COMMAND = 'notify-send "Alarm %I: %C"'

def print_error(msg):
  print('\033[31m[ERROR]\033[0m ' + msg)

def list_files(dir):
  try:
    _,_,files = next(walk(dir))
  except StopIteration:
    files = []
  
  return files