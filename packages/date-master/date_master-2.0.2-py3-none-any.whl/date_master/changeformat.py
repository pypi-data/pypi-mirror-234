from .numbertoword import convert
from .validation import *


def changeformat(date, order, format):
    try:
        count = 0
        for count in range(len(order)):

            if order[count] == 'DD':
                if format[count] == 'str':
                    word = convert(date[count])
                    date[count] = word                
                count += 1

            elif order[count] == 'MM':
                if format[count] == 'str':
                    word = month_constants.get(date[count])
                    date[count] = word
                count += 1        
            
            elif order[count] == 'YYYY':
                if format[count] == 'str':
                    word = convert(date[count])
                    date[count] = word
                count += 1
        return date
    except Exception as e:
        message = str(e)
        return message


def changeformat_without_order(date, format):
    try:
        count = 0
        for count in range(len(date)):

            if count == 0:
                if format[count] == 'str':
                    word = convert(date[count])
                    date[count] = word                
                count += 1

            elif count == 1:
                if format[count] == 'str':
                    word = month_constants.get(date[count])
                    date[count] = word
                count += 1        
            
            elif count == 2:
                if format[count] == 'str':
                    word = convert(date[count])
                    date[count] = word
                count += 1
        return date
    except Exception as e:
        message = str(e)
        return message