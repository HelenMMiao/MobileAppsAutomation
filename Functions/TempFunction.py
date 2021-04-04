alarmSet = ['8:30', 'am']
def tempTest():
    global alarmSet
    alarmH = alarmSet[0].split(':')[0]
    print(alarmH)

tempTest()