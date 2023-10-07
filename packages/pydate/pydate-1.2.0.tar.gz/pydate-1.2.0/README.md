# ***pydate***

    Python package made to set, parse, & format DateTime objects.

    Python version 3.6 is required at a minimum.  

    To install the package with pip enter command in terminal:
        pip install pydate

    To uninstall the package with pip enter command in terminal:
        pip uninstall pydate

    Note: All object params are optional. Their values are set None without constructor. 

## ***Module Year***

<table width="100%">
	<tr>
		<th align="left">
            Attribute/Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
	<tr>
		<td>
            <code>year</code>
        </td>
		<td>
            Attribute of the int type representing a year. <br/>
            The attribute must be 4 digits.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_year()</code>
        </td>
		<td>
            Return the year attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_year(year)</code>
        </td>
		<td>
            Set the year attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_year_UTC()</code>
        </td>
		<td>
            Set the year attribute to the current UTC year.
        </td>
	</tr>
    <tr>
		<td>
            <code>tostring()</code>
        </td>
		<td>
            Return a string representing the Year class attribute values.
        </td>
	</tr>
</table>

---

## ***Module Date***

    Note: This class inherits the attributes/methods of the Year class. 

<table width="100%">
	<tr>
		<th align="left">
            Attribute/Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
	<tr>
		<td>
            <code>month</code>
        </td>
		<td>
            Attribute of the int type representing a month. <br/>
            The attribute's value must be between 1 & 12.
        </td>
	</tr>
    <tr>
		<td>
            <code>day</code>
        </td>
		<td>
            Attribute of the int type representing a day. <br/>
            The attribute's value must be between 1 & 31.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_month()</code>
        </td>
		<td>
            Return the month attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_day()</code>
        </td>
		<td>
            Return the day attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_gregorian()</code>
        </td>
		<td>
            Return the Gregorian month name.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_total_days()</code>
        </td>
		<td>
            Return a dictionary denoting the total days in each month. <br/> Uses each gregorian month name as a key.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_month(month)</code>
        </td>
		<td>
            Set the month attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_month_UTC()</code>
        </td>
		<td>
            Set the month attribute to the current UTC month.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_day(day)</code>
        </td>
		<td>
            Set the day attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_day_UTC()</code>
        </td>
		<td>
            Set the day attribute to the current UTC day.
        </td>
	</tr>
    <tr>
		<td>
            <code>tostring()</code>
        </td>
		<td>
            Return a string representing the Date class attribute values.
        </td>
	</tr>
</table>

---

## ***Module Time***

<table width="100%">
	<tr>
		<th align="left">
            Attribute/Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
	<tr>
		<td>
            <code>hour</code>
        </td>
		<td>
            Attribute of the int type representing a hour. <br/>
            The attribute's value must be between 0 & 23.
        </td>
	</tr>
    <tr>
		<td>
            <code>minute</code>
        </td>
		<td>
            Attribute of the int type representing a minute. <br/>
            The attribute's value must be between 0 & 59.
        </td>
	</tr>
    <tr>
		<td>
            <code>second</code>
        </td>
		<td>
            Attribute of the int type representing a second. <br/>
            The attribute's value must be between 0 & 59.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_hour()</code>
        </td>
		<td>
            Return the hour attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_minute()</code>
        </td>
		<td>
            Return the minute attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_second()</code>
        </td>
		<td>
            Return the second attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_hour(hour)</code>
        </td>
		<td>
            Set the hour attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_hour_UTC()</code>
        </td>
		<td>
            Set the hour attribute to the current UTC hour.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_minute(minute)</code>
        </td>
		<td>
            Set the minute attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_minute_UTC()</code>
        </td>
		<td>
            Set the minute attribute to the current UTC minute.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_second(second)</code>
        </td>
		<td>
            Set the second attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_second_UTC()</code>
        </td>
		<td>
            Set the second attribute to the current UTC second.
        </td>
	</tr>
    <tr>
		<td>
            <code>tostring()</code>
        </td>
		<td>
            Return a string representing the Time class attribute values.
        </td>
	</tr>
</table>

---

## ***Module DateTime***

    Note: This class inherits the attributes/methods of both the Date & Time classes.

<table width="100%">
	<tr>
		<th align="left">
            Attribute/Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
    <tr>
		<td>
            <code>set_UTC()</code>
        </td>
		<td>
            Set second, minute, hour, day, month, and year attribute values to current UTC values.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_timezone(timezone)</code>
        </td>
		<td>
            Set second, minute, hour, day, month, and year attribute values to values of timezone indicated in the argument.
            The 'timezone' argument must be a string. <br/>
            Values for the 'timezone' argument can be the following acronyms (Not Case Sensitive): <br/>
                - AST => (Atlantic Standard Time UTC-04:00) <br/>
                - EDT => (Eastern Daylight Time UTC-04:00) <br/>
                - EST => (Eastern Standard Time UTC-05:00) <br/>
                - CDT => (Central Daylight Time UTC-05:00) <br/>
                - CST => (Central Standard Time UTC-06:00) <br/>
                - MDT => (Mountain Daylight Time UTC-06:00) <br/>
                - MST => (Mountain Standard Time UTC-07:00) <br/>
                - PDT => (Pacific Daylight Time UTC-07:00) <br/>
                - PST => (Pacific Standard Time UTC-08:00) <br/>
                - AKDT => (Alaska Daylight Time UTC-08:00) <br/>
                - AKST => (Alaska Standard Time UTC-09:00) <br/>
                - HDT => (Hawaii-Aleutian Daylight Time UTC-09:00) <br/>
                - HST => (Hawaii-Aleutian Standard Time UTC-10:00) <br/>
                - SST => (Samoa Standard Time UTC-11:00)
        </td>
	</tr>
	<tr>
		<td>
            <code>tostring()</code>
        </td>
		<td>
            Return a string representing the DateTime class attribute values.
        </td>
	</tr>
</table>

[Back to Top](#pydate)

---
