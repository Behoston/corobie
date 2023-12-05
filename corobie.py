import calendar
import datetime
import os
import pathlib
import re
import subprocess

today = datetime.date.today()
first_day = today.replace(day=1) - datetime.timedelta(days=1)
_, last_day_of_month = calendar.monthrange(today.year, today.month)
last_day = datetime.date(today.year, today.month, last_day_of_month) + datetime.timedelta(days=1)
cwd = pathlib.Path(os.getcwd())
dates = set()
total_hours = 0
for directory in cwd.iterdir():
    if not directory.is_dir() or not (directory / '.git').is_dir():
        continue
    try:
        reflog = subprocess.check_output(
            ['git', 'reflog', f'--since={first_day}', f'--until={last_day}', '--date=iso'],
            stderr=subprocess.DEVNULL,
            cwd=directory,
        ).decode()
    except Exception as ignored:
        continue
    dates.update(re.findall(r'\d{4}-\d\d?-\d\d?', reflog))

current_day = today.replace(day=1)


def print_color(text: str, color_code: int):
    print(f"\033[{color_code}m{text}\033[00m")


while current_day.month == today.month:
    s = str(current_day)
    if current_day.isoweekday() in (6, 7):
        print_color(s, 37)
    elif s in dates:
        print_color(s, 32)
        total_hours += 8
    else:
        print_color(s, 31)
    current_day = current_day + datetime.timedelta(days=1)
print_color(f"Total hours: {total_hours}", 34)
