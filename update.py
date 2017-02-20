import requests

def main():
    url = "http://voenmeh.ru/students/timetable/TimetableGroup.xml"
    response = requests.get(url)
    schedule = open('schedule.xml', 'w+')
    schedule.write(response.text)
    schedule.close()

if __name__ == '__main__':
    main()
