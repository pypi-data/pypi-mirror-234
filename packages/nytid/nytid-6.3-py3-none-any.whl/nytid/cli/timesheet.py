import arrow
import canvasapi
import canvaslms.cli
import csv
import config
from nytid.signup import hr
from nytid.signup.hr import timesheet
from nytid.signup import sheets
import ladok3.kth
import operator
import os
import sys

def get_ladok_id(user, students):
    """
    Translates user ID to LADOK ID.
    - `user` is the username.
    - `students` is a list of students from Canvas (canvasapi.student.Student)
    """
    for student in students:
        if student.login_id == user:
            return student.integration_id
    raise KeyError(f"can't find {user}")

def to_hours(td):
    """
    Converts timedelta to hours.
    """
    return td.total_seconds()/60/60

def summarize_user(user, course, course_events,
                   salary=150):
    """
    Returns events where TA worked.
    - `user` is the TA's username.
    - `course` is the course code.
    - `course_events` is a list of events.
    - Optional `salary` is the hourly salary.
    """
    hours = to_hours(hr.hours_per_TA(course_events)[user])

    start_idx = sheets.SIGNUP_SHEET_HEADER.index("Start")
    end_idx = sheets.SIGNUP_SHEET_HEADER.index("End")
    type_idx = sheets.SIGNUP_SHEET_HEADER.index("Event")

    events = sheets.filter_events_by_TA(user, sorted(course_events,
            key=operator.itemgetter(start_idx)))
    events = filter(lambda x: user in sheets.get_booked_TAs_from_csv(x)[0], 
                    events)
    events = list(map(lambda x: x[0:len(sheets.SIGNUP_SHEET_HEADER)] + [user], 
                      events))

    xl_events = []

    for event in events:
        end = arrow.get(event[end_idx])
        start = arrow.get(event[start_idx])
        event_type = event[type_idx]
        time = end-start
        time_with_prep = to_hours(hr.round_time(
                                hr.add_prep_time(time, event_type,
                                                 date=start.date())))

        xl_events.append({
                "datum": str(start.date()),
                "tid": str(start.time()),
                "kurskod": course,
                "typ": event_type,
                "timmar": to_hours(time),
                "koeff": hr.prep_factor(event_type, date=start.date(),
                                        amanuensis=False),
                "omr_tid": time_with_prep,
                "belopp": time_with_prep * salary
            })

    return xl_events


def main():
    """
    Main command code
    """
    cs = canvasapi.Canvas(os.environ["CANVAS_SERVER"], 
                          os.environ["CANVAS_TOKEN"])
    ls = ladok3.kth.LadokSession(os.environ["KTH_LOGIN"],
                                 os.environ["KTH_PASSWD"])

    course = next(canvaslms.cli.courses.filter_courses(cs, "datintro22"))
    students = list(course.get_users())

    course_events = []

    for course, url in config.SIGNUP.items():
        course_events += sheets.read_signup_sheet_from_url(url)

    if len(sys.argv) > 1:
        users = sys.argv[1:]
    else:
        users = hr.hours_per_TA(course_events)

    for user in users:
        try:
            ta = ls.get_student(get_ladok_id(f"{user}@kth.se", students))
        except KeyError as err:
            print(f"can't look up {user} in LADOK: {err}")
            continue

        ta_events = summarize_user(user, course, course_events)
        try:
            timesheet.make_xlsx(ta.personnummer,
                                f"{ta.first_name} {ta.last_name}",
                                f"{user}@kth.se",
                                ta_events,
                                course_leader=("Daniel Bosk", "dbosk@kth.se"),
                                HoD="Karl Meinke",
                                org="JH", project="1102",
                                course_leader_signature="~/Pictures/signature.png")
        except AttributeError as err:
            print(f"can't access {user}'s LADOK data: {err}")
            continue

if __name__ == "__main__":
    main()
