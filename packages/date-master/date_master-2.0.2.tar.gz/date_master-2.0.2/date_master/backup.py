# from exceptions import *


# def validation(date):
#     try:
#         if len(date) == 3:
#             for item in range(len(date)):
#                 if item == 0:
#                     if isinteger(date[item]) and checklimit(date[item], 'DD') == True:
#                         pass
#                     else:
#                         eroorr = InvalidDayError
#                         raise eroorr
#                 elif item == 1:
#                     if isinteger(date[item]) and checklimit(date[item], 'MM') == True:
#                         pass
#                     else:
#                         raise InvalidMonthError
#                 elif item == 2:
#                     if isinteger(date[item]) and checklimit(date[item], 'YYYY') == True:
#                         return True
#                     else:
#                         raise InvalidYearError
#                 else:
#                     raise InvalidDateError
#         else:
#             raise InvalidDateError

#     except InvalidDayError:
#         print('Invalid day')

#     except InvalidMonthError:
#         print('Invalid month')

#     except InvalidYearError:
#         print('Invalid year')

#     except InvalidDateError:
#         print('Invalid date')

