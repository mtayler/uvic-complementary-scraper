#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
import urllib

class_months = ["09", "01"]

def getTitleOld(dept, num, year):
    url = "http://web.uvic.ca/calendar{}/CDs/{}/{}.html".format(year, dept, num)
    try:
        sock = urllib.request.urlopen(url)
        page = sock.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            if year > 2010:
                return getTitleOld(dept, num, year-1)
            else:
                print("{} {}: Couldn't find class".format(dept, num))
                return
        else:
            raise e

    sock.close()
    soup = bs(page, "lxml")
    return soup.find('div', {'id': 'CDpage'}).find('h2').text


def getTitle(dept, num, year, month):
    url = "http://web.uvic.ca/calendar{}-{}/CDs/{}/{}.html".format(year, class_months[month], dept, num)
    try:
        sock = urllib.request.urlopen(url)
        page = sock.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            if month == 1:
                if year > 2014:
                    return getTitle(dept, num, year-1, 0)
                else:
                    return getTitleOld(dept, num, year-1)
            else:
                return getTitle(dept, num, year, 1)

        else:
            raise e

    sock.close()
    soup = bs(page, "lxml")
    if year > 2015:
        return soup.find('h2', {'class': 'course-title'}).text
    else:
        return soup.find('div', {'id': 'CDpage'}).find('h2').text

with open("/media/sf_D_DRIVE/uvic-comp-list", 'r') as class_list:
    with open("/media/sf_D_DRIVE/uvic-complementary-classes.txt", 'w') as out:
        last_dept = ""
        for line in class_list:
            dept, num, *other = line.rstrip('\n').split(' ')
            if last_dept != dept:
                print()
                print(dept, end=" ")
            print(num, end=" ")
            last_dept = dept
            title = getTitle(dept, num, 2017, 0)
            out.write("{:>4} {:<3}\t{}\n".format(dept, num, title))
        print()

