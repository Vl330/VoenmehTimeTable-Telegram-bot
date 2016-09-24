# -*- coding: utf-8 -*

import datetime
from lxml import etree


def get_week(group_name):
    tree = etree.parse('schedule.xml')
    root = tree.getroot()
    group = root.find('.//Group[@Number="{}"]'.format(group_name.upper()))
    if group is None:
        return "Нет такой группы."
    semester = root.find('./Period').items()
    year = int(semester[1][1])
    month = int(semester[2][1])
    day = int(semester[3][1])
    week = group.findall('.//Day')
    start = datetime.date(year, month, day)
    now = datetime.date.today()
    delta_weeks = (now - start).days // 7
    parity = 'Нечетная' if delta_weeks % 2 == 0 else 'Четная'
    return week, parity


def get_day(timetable):
    if isinstance(timetable, str):
        return timetable
    info = ""
    schedule, parity = timetable
    for day in schedule:
        day_name = day.find('.//DayTitle').text
        info += "\n{}\n".format(day_name)
        for lesson in day.findall('.//Lesson'):
            if parity in lesson.find('Time').text:
                time = lesson.find('Time').text.split()[0]
                subj = lesson.find('Discipline').text
                try:
                    teacher = lesson.find('.//ShortName').text
                except AttributeError:
                    teacher = ""
                room = lesson.find('.//Classroom').text
                if room is None:
                    room = ""
                info += "{} {} {} {} \n".format(time, subj, teacher, room)
    return info


def today(group_num):
    date = datetime.date.today()
    day_num = date.weekday()
    week = get_week(group_num)
    if isinstance(week, str):
        return week
    true_week = week[0]
    try:
        day = true_week[day_num]
    except IndexError:
        return "Сегодня пар нет."
    parity = week[1]
    return day, parity

