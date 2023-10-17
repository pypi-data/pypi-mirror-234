import arrow.arrow as arrow
import calendar
import dateutil
import ics.event
import ics.icalendar
import requests

TIMEEDIT_EVENTS = [
    "Datorlaboration",
    "Computer lab",
    "Examination",
    "Exkursion",
    "Excursion",
    "Fältövning",
    "Field exercise",
    "Frågestund",
    "Question time",
    "Question Time",
    "Föreläsning",
    "Lecture",
    "FX-komplettering",
    "FX-completion",
    "Handledning",
    "Tutorial",
    "Information",
    "Kontrollskrivning",
    "Partial Exam/Quiz",
    "Laboration",
    "Lab",
    "Lektion",
    "Lesson",
    "Omtenta",
    "Re-exam",
    "Re-Exam",
    "Presentation",
    "Projektarbete",
    "Project work",
    "Project Work",
    "Redovisning",
    "Reporting",
    "Räknestuga",
    "Math work session",
    "Seminarium",
    "Seminar",
    "Samverkansinlärning",
    "Supplemental instruction",
    "Supplemental Instruction",
    "Studiebesök",
    "Study visit",
    "Tentamen",
    "Exam",
    "Upprop",
    "Roll-call",
    "Webinarium",
    "Webinar",
    "Verksamhetsförlagd utbildning",
    "Pre-service Placement",
    "Workshop",
    "Övning",
    "Exercise",
]


def format_header(event):
    """
    Formats the event header, a one-line representation (week, date, time,
    event title)
    """
    header = (
        f"Week {event.begin.isocalendar()[1]} "
        + calendar.day_name[event.begin.weekday()]
        + " "
        + event.begin.to(dateutil.tz.tzlocal()).format("DD/MM HH:mm")
    )

    header += f" {event.name}"

    return header


def format_event(event):
    """
    Takes event (ics.event.Event) object,
    returns long string representation (header, location, description over
    several lines)
    """
    header = format_header(event)
    location = event.location
    description = "\n".join(
        filter(lambda x: "http" not in x, event.description.splitlines())
    )

    return f"{header}\n{location}\n{description}".strip()


def filter_event_description(
    event_desc, ignore=["http", "grupp", "group", "ID ", "Daniel Bosk"], separator="; "
):
    """
    Takes event description event_desc as string,
    returns filtered string with newlines replaced by semicolons.
    Rows of description containing any term in list ignore, will not appear in
    the returned string.
    The filtered rows of the description are joined again by the string in
    separator.
    """
    desc_parts = event_desc.splitlines()
    desc_parts_keep = []

    for part in desc_parts:
        found = False
        for term in ignore:
            if term in part:
                found = True
                break

        if not found:
            desc_parts_keep.append(part)

    return separator.join(desc_parts_keep)


def format_event_short(event):
    """Takes event (ics.event.Event) object,
    returns a short string representation (one line)"""
    header = format_header(event)
    description = filter_event_description(event.description)

    return f"{header} {description}".strip()


def read_calendar(url):
    """
    Input: url is a string containing the URL to the ICS-formatted calendar.
    Output: an [[ics.icalendar.Calendar]] object.
    """
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return ics.icalendar.Calendar(imports=response.text)
    raise Exception(response.text)


def event_filter(events, whitelisted=TIMEEDIT_EVENTS):
    """
    Takes a list of events (ics.event.Event), returns a filtered list of events
    (generator). The events to include are the teaching events.

    It covers the following events:

      "Datorlaboration", "Computer lab",
      "Examination",
      "Exkursion", "Excursion",
      "Fältövning", "Field exercise",
      "Frågestund", "Question time", "Question Time",
      "Föreläsning", "Lecture",
      "FX-komplettering", "FX-completion",
      "Handledning", "Tutorial",
      "Information",
      "Kontrollskrivning", "Partial Exam/Quiz",
      "Laboration", "Lab",
      "Lektion", "Lesson",
      "Omtenta", "Re-exam", "Re-Exam",
      "Presentation",
      "Projektarbete", "Project work", "Project Work",
      "Redovisning", "Reporting",
      "Räknestuga", "Math work session",
      "Seminarium", "Seminar",
      "Samverkansinlärning", "Supplemental instruction",
      "Supplemental Instruction",
      "Studiebesök", "Study visit",
      "Tentamen", "Exam",
      "Upprop", "Roll-call",
      "Webinarium", "Webinar",
      "Verksamhetsförlagd utbildning", "Pre-service Placement",
      "Workshop",
      "Övning", "Exercise"
    """
    for event in events:
        for event_type in whitelisted:
            if event_type in event.name:
                yield event
                break
