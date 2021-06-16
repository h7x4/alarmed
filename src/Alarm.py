from datetime import datetime
from json import dump, load
from uuid import uuid4
from os import walk, path

from common import PREVIOUS_ALARM_DIR, ALARM_DIR, list_files

class Alarm:
  def __init__(self, timestamp, comment=None, command=None, id=None):
    self.timestamp = timestamp
    self.comment = comment
    self.command = command
    self.id = id or self.generateId()

  def __str__(self):
    return str(self.__dict__)

  @classmethod
  def readFromFile(cls, path):
    with open(path) as file:
      data = load(file)
      alarm = cls(data['timestamp'], data['comment'], data['command'], data['id'])
      return alarm

  def writeToFile(self, path):
    with open(path, 'w') as file:
      dump(self.__dict__, file)
  
  def generateId(self):
    alarm_files = list_files(ALARM_DIR)
    prev_alarm_files = list_files(PREVIOUS_ALARM_DIR)

    i = 1
    while hex(i)[2:].upper() in alarm_files + prev_alarm_files:
      i += 1

    return hex(i)[2:].upper()
  
  def getTimeLeft(self):
    timeleft = datetime.fromtimestamp(self.timestamp) - datetime.now()
    hs = str(timeleft.seconds // 3600).zfill(2)
    ms = str((timeleft.seconds // 60) % 60).zfill(2)
    ss = str(timeleft.seconds % 60).zfill(2)
    if timeleft.days:
      return f'{timeleft.days} days, {hs}:{ms}:{ss}'
    else:
      return f'{hs}:{ms}:{ss}'