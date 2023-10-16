
def change_order(date,order):
    try:
        day = date[0]
        month = date[1]
        year = date[2]

        order_1 = order[0]
        order_2 = order[1]
        order_3 = order[2]

        new_date = []
        

        if order_1 == 'DD':
            if order_2 == 'MM':
                new_date.append(day)
                new_date.append(month)
                new_date.append(year)
            elif order_2 == 'YYYY':
                new_date.append(day)
                new_date.append(year)
                new_date.append(month)
            return new_date
            
        elif order_1 == 'MM':
            if order_2 == 'DD':
                new_date.append(month)
                new_date.append(day)
                new_date.append(year)
            elif order_2 == 'YYYY':
                new_date.append(month)
                new_date.append(year)
                new_date.append(day)
            return new_date

        elif order_1 == 'YYYY':
            if order_2 == 'DD':
                new_date.append(year)
                new_date.append(day)
                new_date.append(month)
            elif order_2 == 'MM':
                new_date.append(year)
                new_date.append(month)
                new_date.append(day)
            return new_date
        else:
            return 0
    except Exception as e:
        message = str(e)
        return message