=======================

Date master is a python library which helps you to manage and display your entered date based on your project requirement. Just take a look into the use cases of date master. 

    1)  Get the current date 
    2)  Get the current day, month and year 
    3)  Get the date 'n' days before and after from the current date 
    4)  Get the date 'n' days before and after from the custom date 
    5)  Change the order of date 
            Eg: dd/mm/yyyy to yyyy/mm/dd
    6)  Change the format of your date(integer to string or string to interger)
            Eg: 31/8/2022 to 31/August/Two Thousand and Twenty Two
    7)  Change the split value
            Eg: 31 / 8 / 2022 to 31 | 8 | 2022
    8)  Compare two dates(==, <, <=, >, >=)
    9)  Check wether the year is leapyear or not



**Parameters**


beautiful_date() parameters

    1)  date = Date that you have entered(value type = Integer)
    2)  order = Specifies the order of your date that you want to display(value type = String)
    3)  format = Specifies the format of your date that you want to display string(str) or integer(int)(value type = String)
    4)  split_by = Specifies the split value(value type = String)


get_date parameters and methods

    1)  today() = Get the current date
        1.1)  today(n) = Get the date 'n' days after from the current date
        1.2)  today(-n) = Get the date 'n' days before from the current date
    2)  day() = Get the current day
    3)  month() = Get the current month
    4)  year() = Get the current year


check_date parameters and methods

    1)  compare('date1','operator','date2') = Compare two dates
        1.1)  compare('date1', '==', 'date2') = Check wether the date1 and date2 are equal
        1.2)  compare('date1', '<', 'date2') = Check wether the date1 is less than date2
        1.3)  compare('date1', '<=', 'date2') = Check wether the date1 is less than or equal to date2
        1.4)  compare('date1', '>', 'date2') = Check wether the date1 greater than date2
        1.5)  compare('date1', '>=', 'date2') = Check wether the date1 is greater than or equal to date2
    2)  isleapyear(year) = check wether the year is leapyear or not


**Constraints**


beautiful_date() constraints

    1)  beautiful_date param must be a dict of values
    2)  'date' is a mandatory param for all your request in dd,mm,yyyy format


get_date constraints

    1)  Get date have multiple methods they are today(), day(), month(), year()
    2)  today() is the only method have parameter. It will be a positive or negative number "represented by minus sign" or leave as empty


check_date constraints

    1)  check_date consist two methods they are compare() and isleapyear()
    2)  compare need 3 parameters and they are in the order date1, operator, date2
        2.1)  date1 and date2 is a custom date or current date. current date represented by the string 'today'
        2.2)  operators are equalto(==), less than(<), less than or equalto(<=), greater than(>), greater than or equalto(>=)
    3)  isleapyear(year) have only one parameter. It will be a positive integer value.



Installing
=======================
    
    pip install date-master

Usage - beautiful_date()
=======================

    from date_master.date import beautiful_date
    
    date = ['today'] or # current date
           ['today',2] or # date after 2 days from the current date
           ['today',-10] # date before 10 days from the current date

           [31, 8, 2022] or # Custom date
           [[31, 8, 2022],2] or # date after 2 days from the custom date
           [[31, 8, 2022],-10] or # date before 10 days from the custom date
           
    order = ['DD','YYYY','MM']
    format = ['int','str','str']
    split_by = ['|']


    params = {
        'date':date,
        'order':order,
        'format':format,
        'split_by':split_by
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> 31| 'Two Thousand and Twenty Two'| 'August'
 

**Usecase 1** :- Get the current date

Constraints : 
    date contain a value that must be 'today'

    date = ['today']

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [31, 8, 2022]


**Usecase 2** :- Get date after 2 days from the current date

Constraints : 
    date contain 2 value that must be 'today' and the number of days from current date

    date = ['today', 2]

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [2, 9, 2022]


**Usecase 3** :- Get date before 10 days from the current date

Constraints : 
    date contain 2 value that must be 'today' and the number of days from current date. Second value must be negative integer

    date = ['today', -10]

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [21, 8, 2022]



**Usecase 4** :- Custom date

Constraints : 
    date contain a value that must be your date

    date = [31, 8, 2022]

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [31, 8, 2022]


**Usecase 5** :- Get date after 2 days from the custom date

Constraints : 
    date contain 2 value that must be your custom date and the number of days from that date

    date = [[31, 8, 2022], 2]

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [2, 9, 2022]


**Usecase 6** :- Get date before 10 days from the custom date

Constraints :
    date contain 2 value that must be your custom date and the number of days from that date. Second value must be negative integer

    date = [[31, 8, 2022], -10]

    params = {
        'date':date
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [21, 8, 2022]


**Usecase 7** :- Changing the 'order' of date

Constraints : 
    order list contain 3 values that must be 'dd','mm', and 'yyyy'

    date = [31, 8, 2022]
    order = ['YYYY','DD','MM']

    params = {
        'date':date,
        'order':order
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [2022, 31, 8]


**Usecase 8** :- Changing the date 'format'

Constraints : 
    format contain 3 values that must be 'str' or 'int'

    date = [31, 8, 2022]
    format = ['int','str','str']

    params = {
        'date':date,
        'format':format
    }

    result = beautiful_date(params)
    print(result)

    Result
    ====================
    >> [31, 'August', 'Two Thousand and Twenty Two']


**Usecase 9** :- Changing the 'split_by' value of date

Constraints : 
    split_by contain a single value, it must be a string

    date = [31, 8, 2022]
    split_by = ['|']

    params = {
        'date':date,
        'split_by':split_by
    }

    result = beautiful_date(params)
    print(result)
    
    Result
    ====================
    >> [31| 8| 2022]


Usage - get_date
=======================
    
    from date_master.date import get_date

    result = get_date.method_name()
    print(result)
    
    Result
    ====================
    >> [31, 8, 2022]
 

**Usecase 1** :- Get the current date 

    result = get_date.today()
    print(result)
    
    Result
    ====================
    >> [31, 8, 2022]


**Usecase 2** :- Get the date 5 days after from the current date 

    result = get_date.today(5)
    print(result)
    
    Result
    ====================
    >> [5, 9, 2022]


**Usecase 3** :- Get the date 5 days before from the current date 

    result = get_date.today(-5)
    print(result)
    
    Result
    ====================
    >> [26, 8, 2022]

**Usecase 4** :- Get the current day 

    result = get_date.day()
    print(result)
    
    Result
    ====================
    >> 31

**Usecase 5** :- Get the current month 

    result = get_date.month()
    print(result)
    
    Result
    ====================
    >> 8

**Usecase 6** :- Get the current year 

    result = get_date.year()
    print(result)
    
    Result
    ====================
    >> 2022


Usage - check_date
=======================
    
    from date_master.date import check_date

    result = check_date.method_name()
    print(result)
    
    Result
    ====================
    >> True or False


 **Usecase 1** :- Check wether both date are equal 

    result = check_date.compare('31/08/2022','==','31/08/2022')
    print(result)
    
    Result
    ====================
    >> True

 **Usecase 2** :- Check wether the date1 is less than date2 

    result = check_date.compare('31/08/2022','<','30/08/2022')
    print(result)
    
    Result
    ====================
    >> False

 **Usecase 3** :- Check wether the date1 is less than or equal to date2

    result = check_date.compare('31/08/2022','<=','31/08/2022')
    print(result)
    
    Result
    ====================
    >> True

 **Usecase 4** :- Check wether the date1 is greater than date2 

    result = check_date.compare('31/08/2022','>','01/09/2022')
    print(result)
    
    Result
    ====================
    >> False

 **Usecase 5** :- Check wether the date1 is greater than or equal to date2 

    result = check_date.compare('01/09/2022','>=','01/09/2022')
    print(result)
    
    Result
    ====================
    >> True

 **Usecase 6** :- Check wether the year is leapyear or not

    result = check_date.isleapyear(2000)
    print(result)
    
    Result
    ====================
    >> True