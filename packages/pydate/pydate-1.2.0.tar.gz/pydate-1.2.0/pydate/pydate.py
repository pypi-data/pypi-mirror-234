#!/usr/bin/env python3

from datetime import datetime

class Year:

    # Constructor
    def __init__(self, year = None):
        if (year is not None): 
            if (type(year) is not int):
                raise TypeError("The year argument isn't an int!")

            if (len(str(year)) < 4):
                raise ValueError("The year argument must have 4 or more digits!")

        self.year = year

    # Return the year attribute value. 
    def get_year(self):
        return self.year

    # Set the year attribute value.
    def set_year(self, year):
        if (type(year) is not int):
            raise TypeError("The year argument isn't an int!")

        if (len(str(year)) < 4):
            raise ValueError("The year argument must have 4 or more digits!")

        self.year = year

    # Set the year attribute to the current UTC year.
    def set_year_UTC(self):
        self.year = datetime.utcnow().year

    # Return a string representing the Year class attribute values.
    def tostring(self):
        return str(self.year)

class Date(Year):

    # Constructor
    def __init__(self, year = None, month = None, day = None):
        super().__init__(year)

        if (month is not None): 
            if (type(month) is not int):
                raise TypeError("The month argument isn't an int!")

            if (month < 1 or month > 12):
                raise ValueError("The month argument must be between 1 and 12!")

        if (day is not None): 
            if (type(day) is not int):
                raise TypeError("The day argument isn't an int!")

            if (day < 1 or day > 31):
                raise ValueError("The day argument must be between 1 and 31!")

        self.month = month
        self.day = day

    # Return the month attribute value. 
    def get_month(self):
        return self.month

    # Return the day attribute value. 
    def get_day(self):
        return self.day

    # Return the Gregorian month name.
    def get_gregorian(self):
        if (self.month == 1):
            return "January"
        elif (self.month == 2):
            return "February"
        elif (self.month == 3):
            return "March"
        elif (self.month == 4):
            return "April"
        elif (self.month == 5):
            return "May"
        elif (self.month == 6):
            return "June"
        elif (self.month == 7):
            return "July"
        elif (self.month == 8):
            return "August"
        elif (self.month == 9):
            return "September"
        elif (self.month == 10):
            return "October"
        elif (self.month == 11):
            return "November"
        elif (self.month == 12):
            return "December"
        else:
            return None

    # Return a dictionary denoting the total days in each month. Uses each gregorian month name as a key.
    def get_total_days(self):
        total_days = dict({
            "January": 31,
            "February": 28,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31, 
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        })

        return total_days

    # Set the month attribute value. 
    def set_month(self, month):
        if (type(month) is not int):
            raise TypeError("The month argument isn't an int!")

        if (month < 1 or month > 12):
            raise ValueError("The month argument must be between 1 and 12!")

        self.month = month

    # Set the month attribute to the current UTC month.
    def set_month_UTC(self):
        self.month = datetime.utcnow().month

    # Set the day attribute value.
    def set_day(self, day):
        if (type(day) is not int):
            raise TypeError("The day argument isn't an int!")
        
        if (day < 1 or day > 31):
            raise ValueError("The day argument must be between 1 and 31!")

        self.day = day

    # Set the day attribute to the current UTC day.
    def set_day_UTC(self):
        self.day = datetime.utcnow().day

    # Return a string representing the Date class attribute values. 
    def tostring(self):
        return str(f"{self.year}-{self.month}-{self.day}")

class Time:

    # Constructor
    def __init__(self, hour = None, minute = None, second = None):
        if (hour is not None):
            if (type(hour) is not int):
                raise TypeError("The hour argument isn't an int!")

            if (hour < 0 or hour > 23):
                raise ValueError("The hour argument must be between 0 and 23!")

        if (minute is not None):
            if (type(minute) is not int):
                raise TypeError("The minute argument isn't an int!")

            if (minute < 0 or minute > 59):
                raise ValueError("The minute argument must be between 0 and 59!")

        if (minute is not None):
            if (type(second) is not int):
                raise TypeError("The second argument isn't an int!")

            if (second < 0 or second > 59):
                raise ValueError("The second argument must be between 0 and 59!")

        self.hour = hour
        self.minute = minute
        self.second = second

    # Return the hour attribute value.
    def get_hour(self):
        return self.hour

    # Return the minute attribute value.
    def get_minute(self):
        return self.minute

    # Return the second attribute value.
    def get_second(self):
        return self.second

    # Set the hour attribute value. 
    def set_hour(self, hour):
        if (type(hour) is not int):
            raise TypeError("The hour argument isn't an int!")

        if (hour < 0 or hour > 23):
            raise ValueError("The hour argument must be between 0 and 23!")

        self.hour = hour

    # Set the hour attribute to the current UTC hour.
    def set_hour_UTC(self):
        self.hour = datetime.utcnow().hour

    # Set the minute attribute value.
    def set_minute(self, minute):
        if (type(minute) is not int):
            raise TypeError("The minute argument isn't an int!")

        if (minute < 0 or minute > 59):
            raise ValueError("The minute argument must be between 0 and 59!")

        self.minute = minute
    
    # Set the minute attribute to the current UTC minute.
    def set_minute_UTC(self):
        self.minute = datetime.utcnow().minute

    # Set the second attribute value.
    def set_second(self, second):
        if (type(second) is not int):
            raise TypeError("The second argument isn't an int!")

        if (second < 0 or second > 59):
            raise ValueError("The second argument must be between 0 and 59!")

        self.second = second

    # Set the second attribute to the current UTC second.
    def set_second_UTC(self):
        self.second = datetime.utcnow().second

    # Return a string representing the Time class attribute values. 
    def tostring(self):
        hour = str(self.hour)
        minute = str(self.minute)
        second = str(self.second)

        if (self.hour is not None and self.minute is not None and self.second is not None): 
            if (self.hour <= 9):
                hour = str(0) + hour

            if (self.minute <= 9):
                minute = str(0) + minute

            if (self.second <= 9):
                second = str(0) + second

        return str(f"{hour}:{minute}:{second}")

class DateTime(Date, Time):

    # Constructor
    def __init__(self, year = None, month = None, day = None, hour = None, minute = None, second = None):
        Date.__init__(self, year, month, day)
        Time.__init__(self, hour, minute, second)

    # Set second, minute, hour, day, month, and year attribute values to current UTC values.
    def set_UTC(self):
        DateTime.set_year_UTC(self)
        DateTime.set_month_UTC(self)
        DateTime.set_day_UTC(self)
        DateTime.set_hour_UTC(self)
        DateTime.set_minute_UTC(self)
        DateTime.set_second_UTC(self)

    '''
        Set second, minute, hour, day, month, and year attribute values to values of timezone indicated in the argument.
            The 'timezone' argument must be a string.
            Values for the 'timezone' argument can be the following acronyms (Not Case Sensitive):
                - AST => (Atlantic Standard Time UTC-04:00)
                - EDT => (Eastern Daylight Time UTC-04:00)
                - EST => (Eastern Standard Time UTC-05:00)
                - CDT => (Central Daylight Time UTC-05:00)
                - CST => (Central Standard Time UTC-06:00)
                - MDT => (Mountain Daylight Time UTC-06:00)
                - MST => (Mountain Standard Time UTC-07:00)
                - PDT => (Pacific Daylight Time UTC-07:00)
                - PST => (Pacific Standard Time UTC-08:00)
                - AKDT => (Alaska Daylight Time UTC-08:00)
                - AKST => (Alaska Standard Time UTC-09:00)
                - HDT => (Hawaii-Aleutian Daylight Time UTC-09:00) 
                - HST => (Hawaii-Aleutian Standard Time UTC-10:00)
                - SST => (Samoa Standard Time UTC-11:00)
    '''
    def set_timezone(self, timezone):
        if (type(timezone) is not str):
            raise TypeError('The timezone argument must be a string.')
        
        timezone = str.upper(timezone)
        DateTime.set_UTC(self)

        match timezone:
            case 'AST':
                differential = 4
                DateTime.__decrement_differential(self, differential)
            case 'EDT':
                differential = 4
                DateTime.__decrement_differential(self, differential)
            case 'EST':
                differential = 5
                DateTime.__decrement_differential(self, differential)
            case 'CDT':
                differential = 5
                DateTime.__decrement_differential(self, differential)
            case 'CST':
                differential = 6
                DateTime.__decrement_differential(self, differential)
            case 'MDT':
                differential = 6
                DateTime.__decrement_differential(self, differential)
            case 'MST':
                differential = 7
                DateTime.__decrement_differential(self, differential)
            case 'PDT':
                differential = 7
                DateTime.__decrement_differential(self, differential)
            case 'PST':
                differential = 8
                DateTime.__decrement_differential(self, differential)
            case 'AKDT':
                differential = 8
                DateTime.__decrement_differential(self, differential)
            case 'AKST':
                differential = 9
                DateTime.__decrement_differential(self, differential)
            case 'HDT':
                differential = 9
                DateTime.__decrement_differential(self, differential)
            case 'HST':
                differential = 10
                DateTime.__decrement_differential(self, differential)
            case 'SST':
                differential = 11
                DateTime.__decrement_differential(self, differential)
            case _:
                raise ValueError('The timezone argument must be one of the supported acronyms.')

    # Private helper method used to set hour, day, month, and year values within decrementing UTC timezones.
    def __decrement_differential(self, differential):
        if (DateTime.get_hour(self) < differential):
            if (DateTime.get_day(self) == 1):
                if (DateTime.get_month(self) == 1):
                    DateTime.set_year(self, DateTime.get_year(self) - 1)
                    DateTime.set_month(self, 12)
                    DateTime.set_day(self, DateTime.get_total_days(self)["December"])
                elif (DateTime.get_month(self) == 2):
                    DateTime.set_month(self, 1)
                    DateTime.set_day(self, DateTime.get_total_days(self)["January"])
                elif (DateTime.get_month(self) == 3):
                    DateTime.set_month(self, 2)
                    DateTime.set_day(self, DateTime.get_total_days(self)["February"])
                elif (DateTime.get_month(self) == 4):
                    DateTime.set_month(self, 3)
                    DateTime.set_day(self, DateTime.get_total_days(self)["March"])
                elif (DateTime.get_month(self) == 5):
                    DateTime.set_month(self, 4)
                    DateTime.set_day(self, DateTime.get_total_days(self)["April"])
                elif (DateTime.get_month(self) == 6):
                    DateTime.set_month(self, 5)
                    DateTime.set_day(self, DateTime.get_total_days(self)["May"])
                elif (DateTime.get_month(self) == 7):
                    DateTime.set_month(self, 6)
                    DateTime.set_day(self, DateTime.get_total_days(self)["June"])
                elif (DateTime.get_month(self) == 8):
                    DateTime.set_month(self, 7)
                    DateTime.set_day(self, DateTime.get_total_days(self)["July"])
                elif (DateTime.get_month(self) == 9):
                    DateTime.set_month(self, 8)
                    DateTime.set_day(self, DateTime.get_total_days(self)["August"])
                elif (DateTime.get_month(self) == 10):
                    DateTime.set_month(self, 9)
                    DateTime.set_day(self, DateTime.get_total_days(self)["September"])
                elif (DateTime.get_month(self) == 11):
                    DateTime.set_month(self, 10)
                    DateTime.set_day(self, DateTime.get_total_days(self)["October"])
                elif (DateTime.get_month(self) == 12):
                    DateTime.set_month(self, 11)
                    DateTime.set_day(self, DateTime.get_total_days(self)["November"])
                else:
                    pass
            else:
                DateTime.set_day(self, DateTime.get_day(self) - 1)
        
        new_hour = DateTime.get_hour(self) - differential
        if (new_hour < 0):
            new_hour += 23
        
        DateTime.set_hour(self, new_hour)

    # Return a string representing the DateTime class attribute values.
    def tostring(self):
        hour = str(self.hour)
        minute = str(self.minute)
        second = str(self.second)

        if (self.hour is not None and self.minute is not None and self.second is not None):
            if (self.hour <= 9):
                hour = str(0) + hour

            if (self.minute <= 9):
                minute = str(0) + minute

            if (self.second <= 9):
                second = str(0) + second

        return str(f"{self.year}-{self.month}-{self.day} {hour}:{minute}:{second}")