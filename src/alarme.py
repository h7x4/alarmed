import argparse
from datetime import date, time, datetime, timedelta
from os import walk, path, replace
from pathlib import Path

from Alarm import Alarm
from common import ALARM_DIR, PREVIOUS_ALARM_DIR, print_error, list_files

def get_time_str(file):
  return str(file)

def print_alarms(args):
  files = list_files(ALARM_DIR)

  if files == []:
    print('No alarms')
    return

  if args.id:
    filepath = path.join(ALARM_DIR, args.id)
    if not path.exists(filepath):
      print_error(f'Alarm with id {args.id} does not exist')
    alarms = [Alarm.readFromFile(filepath)]
  else:
    alarms = [Alarm.readFromFile(path.join(ALARM_DIR, file)) for file in files]

  print(args.sep.join(alarm.getTimeLeft() for alarm in alarms))

##### Time input parsers

def parse_clock_time(t): # ex. "-t 18:20"
  time_offset = time(hour=int(t[0:2]), minute=int(t[3:5]))
  time_now = datetime.now()
  time_now_delta = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
  time_offset_delta = timedelta(hours=time_offset.hour, minutes=time_offset.minute, seconds=time_offset.second)

  datetime_today = datetime.combine(date.today(), time(second=0))

  if time_offset_delta > time_now_delta:
    alarm_time = datetime_today + time_offset_delta
  else:
    alarm_time = datetime_today + timedelta(days=1) + time_offset_delta

  return alarm_time

def parse_seconds_time(t): # ex. "-s 3600"
  return datetime.now() + timedelta(seconds=int(t))

def choose_gui_time():
  print('Function not implemented yet')
  exit(1)

def parse_default_time(t):  # ex. "00:40:10"
  time_until_alarm = timedelta(hours=int(t[0:2]), minutes=int(t[3:5]), seconds=int(t[7:9]))
  return datetime.now() + time_until_alarm

#####

def set_alarm(args):
  if args.is_clock_time:
    alarm_time = parse_clock_time(args.time)
  elif args.is_seconds:
    alarm_time = parse_seconds_time(args.time)
  elif args.is_gui:
    alarm_time = choose_gui_time()
  else:
    alarm_time = parse_default_time(args.time)

  alarm = Alarm(alarm_time.timestamp())
  print('Made alarm - ' + str(alarm))
  # print(alarm.getTimeLeft())
  alarm.writeToFile(path.join(ALARM_DIR, alarm.id))

def deactivate_alarm(args):
  file_path = path.join(ALARM_DIR, args.id)
  if not path.exists(file_path):
    print(f'[ERROR] alarm with ID "{args.id}" does not exist')
    exit(1)
  
  replace(file_path, path.join(PREVIOUS_ALARM_DIR, args.id))

def main():
  argparser = argparse.ArgumentParser(description='Get and set alarms for the \'Alarmed\' daemon.')
  argparser.set_defaults(func=lambda _: argparser.print_help())

  # ------------------------------------------------------------------------ #

  subargparsers = argparser.add_subparsers(
    title='subcommands',
    description='Run \'alarme <subcommand> --help\' for more information',
    help='subcommand description')

  # ------------------------------------------------------------------------ #

  get_parser = subargparsers.add_parser('get', help='print out the currently active alarms')
  get_parser.add_argument('-i', '--id', metavar='ID',
                          help='specify the id of the alarm to print')

  get_parser.set_defaults(sep=' | ')
  get_parser.set_defaults(func=print_alarms)

  # ------------------------------------------------------------------------ #

  set_parser = subargparsers.add_parser('set', help='make a new alarm')

  set_time_format_group = set_parser.add_mutually_exclusive_group()
  set_time_format_group.add_argument('-s', '--seconds', dest='is_seconds', action='store_true',
                                    help='specify the remaining time as seconds')
  set_time_format_group.add_argument('-t', '--to', dest='is_clock_time', action='store_true',
                                    help='specify a clock time for the alarm to go off. If the clock is earlier than the current time, it wraps around to tomorrow. Format: "HH:MM"')
  set_time_format_group.add_argument('-g', '--gui', dest='is_gui', action='store_true',
                                    help='use a curses based gui to choose the time')

  set_parser.add_argument('time', metavar='TIME', help='Time until or for the alarm to go off. Default format: "HH:MM:SS"')

  set_parser.add_argument('-c', '--command', metavar='CMD',
                          help='specify a command to run as the alarm goes off')
  set_parser.add_argument('-m', '--message', metavar='MSG',
                          help='add a comment as to what the alarm means')

  set_parser.set_defaults(func=set_alarm)

  # ------------------------------------------------------------------------ #

  deactivation_parser = subargparsers.add_parser('deactivate', help='deactivate one of the alarms')
  deactivation_parser.add_argument('-g', '--gui', dest='is_gui', action='store_true',
                                    help='use a curses based gui to choose an alarm to remove')
  deactivation_parser.add_argument('id', metavar='ID')
  deactivation_parser.set_defaults(func=deactivate_alarm)

  # ------------------------------------------------------------------------ #

  args = argparser.parse_args()

  args.func(args)

if __name__ == '__main__':
  main()