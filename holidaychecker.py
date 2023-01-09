import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


class HolidayChecker:
    def __init__(self, url):
        self._URL = url

    def get_holiday_desc(self):
        r = requests.get(self._URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        search = soup.find(class_="twelve wide column main-body")

        return search

    def get_data_table(self):
        s = self.get_holiday_desc()

        data = s.find("tbody")

        txt = data.text
        data_list = txt.splitlines()

        # Value to be removed
        val = ''

        # Run until the list contains the value
        while val in data_list:
            # Remove the value from the list
            data_list.remove(val)

        return data_list

    def scrape_data(self):
        data_table = self.get_data_table()

        # Used to split the table (similar to the HW1 Question 3)
        updated_list = []
        pre = 0
        new = 2
        for z in range(len(data_table) // 2):
            updated_list.append(data_table[int(pre):int(new)])
            pre = new
            new = new + 2

        check_holiday_dates = []
        for i in range(len(updated_list)):
            if "NO CLASSES" in updated_list[i][1]:
                check_holiday_dates.append(updated_list[i])

        # Since the spring has different format from the fall, I have to format it
        # to look similar
        if "spring" in self._URL:
            check_holiday_dates[0][0] = "January 16"
            for i in range(len(check_holiday_dates)):
                split_format = check_holiday_dates[i][0].split(" ")
                check_holiday_dates[i][0] = split_format[0][:3] + ". " + \
                                            split_format[1]

        return check_holiday_dates

    def get_holidays(self):
        data = self.scrape_data()
        # Used to check for the holiday days
        holiday_dates = []
        # Used to get the year from the given URL
        year = re.findall(r'\d+', self._URL)
        for i in range(len(data)):
            holiday_dates.append(data[i][0] + " " + year[0])

        # Used to format the multiple holiday days
        holiday_dates_update = []
        for i in range(len(holiday_dates)):
            if "-" in holiday_dates[i]:
                multiple_days = re.findall(r'\d+', holiday_dates[i])
                days_difference = int(multiple_days[1]) - int(multiple_days[0])
                count = int(multiple_days[0])
                for j in range(days_difference + 1):
                    count += 1
                    holiday_dates_update.append((holiday_dates[i].split(".")[0] +
                                                 ". " + str(count - 1) + " " + year[
                                                     0] + "-" +
                                                 data[i][1]).split("-"))
            else:
                holiday_dates_update.append(
                    (holiday_dates[i] + "-" + data[i][1]).split("-"))

        return holiday_dates_update

    def is_holiday(self, date):
        holidays = self.get_holidays()

        result = ""
        for i in range(len(holidays)):
            if date in holidays[i][0]:
                result = holidays[i][1]
                return result

        return result
