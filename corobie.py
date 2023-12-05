import datetime
import os
import pathlib
import re
from colorama import Fore
import git
import calendar

today = datetime.date.today()
first_day = today.replace(day=1) - datetime.timedelta(days=1)
_, last_day_of_month = calendar.monthrange(today.year, today.month)
last_day = datetime.date(today.year, today.month, last_day_of_month) + datetime.timedelta(days=1)
cwd = pathlib.Path(os.getcwd())
dates = set()
for directory in cwd.iterdir():
    if not directory.is_dir() or not (directory / '.git').is_dir():
        continue
    repo = git.Repo(directory)
    reflog = repo.git.reflog('--since', first_day, '--until', last_day, '--date', 'iso')
    dates.update(re.findall(r'\d{4}-\d\d?-\d\d?', reflog))

current_day = today.replace(day=1)
while current_day.month == today.month:
    s = str(current_day)
    if current_day.isoweekday() in (6, 7):
        print(Fore.WHITE + s)
    elif s in dates:
        print(Fore.GREEN + s)
    else:
        print(Fore.RED + s)
    current_day = current_day + datetime.timedelta(days=1)
