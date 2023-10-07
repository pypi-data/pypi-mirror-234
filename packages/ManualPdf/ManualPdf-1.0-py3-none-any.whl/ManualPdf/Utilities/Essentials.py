import datetime
import calendar
import base64
import re


class Essentials:

    def __init__(self):
        self.datetime_Format = '%Y%m%d %H:%M:%S.%f'
        self.utc_datetime_Format = '%Y-%m-%dT%H:%M:%S%z'

    def time_print(self, time):
        date_res = datetime.datetime.strptime(time, self.datetime_Format)
        time_strip = datetime.datetime.strptime(time, '%Y%m%d %H:%M:%S.%f').strftime('%H:%M:%S.%f')
        month = calendar.month_abbr[date_res.month]
        year = date_res.year
        day = date_res.day
        a = str(day) + " " + str(month) + " " + str(year) + " " + 'at' + " " + time_strip
        return a

    def utc_time_print(self, time):
        date_res = datetime.datetime.strptime(time, self.utc_datetime_Format)
        time_strip = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M:%S')
        month = calendar.month_abbr[date_res.month]
        year = date_res.year
        day = date_res.day
        a = str(day) + " " + str(month) + " " + str(year) + " " + 'at' + " " + time_strip
        return a

    def time_dff(self, start, end):
        time1 = start
        time2 = end
        diff = datetime.datetime.strptime(time2, self.datetime_Format) \
               - datetime.datetime.strptime(time1, self.datetime_Format)
        date1 = str(diff.seconds)
        date2 = str(diff.microseconds)
        diff1 = str.join('.', (date1, date2))
        return diff1

    def utc_time_dff(self, start, end):
        time1 = start
        time2 = end
        diff = datetime.datetime.strptime(time2, self.utc_datetime_Format) \
               - datetime.datetime.strptime(time1, self.utc_datetime_Format)
        date1 = str(diff.seconds)
        date2 = str(diff.microseconds)
        diff1 = str.join('.', (date1, date2))
        return diff1

    def img_encode(self, path):
        data = open(path, 'rb').read()
        data_base64 = base64.b64encode(data)
        data_base64 = data_base64.decode()
        return data_base64

    def data_encode(self, data):
        data_base64 = base64.b64encode(data)
        data_base64 = data_base64.decode()
        return data_base64

    def remove_special_characters(self, input_string):
        pattern = r'[^a-zA-Z0-9\s]'
        cleaned_string = re.sub(pattern, '', input_string)
        cleaned_string1 = re.sub(r'\s+', ' ', cleaned_string)
        cleaned_string_final = cleaned_string1.replace(' ', '_')
        return cleaned_string_final
