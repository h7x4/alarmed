from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
  name = 'alarmed',
  version = '1.0',
  description = 'A tool to keep track of alarms, and make them execute commands',
  license = 'MIT',
  long_description = long_description,
  author ='h7x4',
  author_email ='h7x4abk3g@protonmail.com',
  url ="https://www.github.com/h7x4ABk3g/alarmed",
  packages = ['alarmed'],
  install_requires = ['xdg', 'python-daemon'],
  entry_points={ 
    'console_scripts': [ 
      'alarme = src.alarme:main',
      'alarmed = src.alarmed:main',
    ] 
  }, 
)