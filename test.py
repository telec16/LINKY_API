import linky
import ids
from pprint import pprint
import datetime

kwhPrice = ids.kwhPrice
rent = ids.rent
m = datetime.date.today().strftime('%m')


def geyAvg(tab):
    avg = 0
    count = 0

    vals = tab['graphe']['data']
    for val in vals:
        if val['valeur'] != -1:
            last = val['valeur']
            avg += last
            count += 1

    if count != 0:
        return avg / count, count, last

    return 0, 0, -1


def printValue(val):
    return str(round(val, 2))


print("Getting 01/" + m + "/2018 to 31/" + m + "/2018")
print("logging in as " + ids.username + "...")
token = linky.login(ids.username, ids.password)
print("logged in successfully")
month = linky._get_data(token, linky.R_ID_MONTH, '01/10/2017', '31/10/2018')
day = linky._get_data(token, linky.R_ID_DAY, '01/' + m + '/2018', '31/' + m + '/2018')

if not (month is None or day is None):
    # pprint(month)
    # pprint(day)

    avgMonth, countMonth, lastMonth = geyAvg(month)
    avgDay, countDay, lastDay = geyAvg(day)

    maxMonth = rent / kwhPrice
    maxDay = maxMonth / 31

    marginMonth = (maxMonth - avgMonth) * countMonth
    marginDay = (maxDay - avgDay) * countDay

    print("\n\n")
    print("Derniers logs> jour : " + printValue(lastDay) + " kwH ; mois : " + printValue(lastMonth) + " kwH\n")
    print("Consomation moyenne journalière : " + printValue(avgDay) + "/" + printValue(maxDay) + " kwH")
    print("Consomation moyenne mensuelle : " + printValue(avgMonth) + "/" + printValue(maxMonth) + " kwH")
    print("Marge pour aujourd'hui : " + printValue(marginDay) + " kwH")
    print("Marge pour ce mois : " + printValue(marginMonth) + " kwH")
    print("\n\n")
