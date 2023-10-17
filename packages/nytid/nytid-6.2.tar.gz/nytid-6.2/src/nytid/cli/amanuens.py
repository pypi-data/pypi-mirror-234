from config import COURSES, SIGNUP
import arrow
import csv
from nytid.signup import hr
from nytid.signup import sheets
import operator
import sys

def to_hours(td):
    return td.total_seconds()/60/60

def shift_dates_forward(start_date, end_date):
    """Takes dates and shifts them so that start_date is tomorrow."""
    now = arrow.now()
    today = arrow.Arrow(now.year, now.month, now.day,
                        hour=start_date.hour, minute=start_date.minute,
                        second=start_date.second)

    if start_date > today:
        return start_date, end_date

    diff = (today-start_date).days
    return start_date.shift(days=diff+1), end_date.shift(days=diff+1)


if len(sys.argv) < 2:
    print(f"{sys.argv[0]}: requires argument 'username'",
          file=sys.stderr)
    print(f"{sys.argv[0]} <username> [<start date>]")
    sys.exit(1)
else:
    user = sys.argv[1]

if len(sys.argv) > 2:
    date = arrow.get(sys.argv[2])
else:
    date = None

booked = []

for course, url in SIGNUP.items():
    booked += sheets.read_signup_sheet_from_url(url)

amanuensis = hr.compute_amanuensis_data(booked,
                                        begin_date=date)
data = amanuensis[user]

#start, end = shift_dates_forward(data[0], data[1])
start = data[0]
end = data[1]

print(f"{user}: {data[2]:.2f} h, "
      f"{round(100*hr.compute_percentage(*data))}%: "
      f"{start.format('YYYY-MM-DD')}--{end.format('YYYY-MM-DD')}")

events = sheets.filter_events_by_TA(user, booked)
events = filter(lambda x: user in sheets.get_booked_TAs_from_csv(x)[0], booked)
events = list(map(lambda x: x[0:len(sheets.SIGNUP_SHEET_HEADER)] + [user], 
                  events))

for event, hours in hr.hours_per_event(events).items():
    print(f"{event}: {to_hours(hours)}")

print()

csvout = csv.writer(sys.stdout)

for event in events:
    csvout.writerow(event)
