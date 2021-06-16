import curses

from common import ALARM_DIR, list_files

def choose_from_list(l):
  screen = curses.initscr()
  screen.addstr(0, 0, "Hello 1 from position (0, 0)")
  screen.addstr(3, 1, "Hello 2 from (3, 1)")
  screen.addstr(4, 4, "X")
  screen.addch(5, 5, "Y")
  screen.refresh()

  curses.napms(2000)
  curses.endwin()
  pass

def choose_clock():
  pass

def choose_alarm_id():
  ids = list_files(ALARM_DIR)
  chosen_id = choose_from_list(ids)
  return chosen_id

if __name__ == '__main__':
  print(choose_alarm_id())