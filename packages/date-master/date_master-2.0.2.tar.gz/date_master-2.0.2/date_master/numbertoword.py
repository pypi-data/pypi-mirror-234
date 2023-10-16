def convertToDigit(n, suffix):
    try:
        EMPTY = ''
        X = [EMPTY, 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ',
            'Eight ', 'Nine ', 'Ten ', 'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ',
            'Fifteen ', 'Sixteen ', 'Seventeen ', 'Eighteen ', 'Nineteen ']
    
        Y = [EMPTY, EMPTY, 'Twenty ', 'Thirty ', 'Forty ', 'Fifty ',
            'Sixty ', 'Seventy ', 'Eighty ', 'Ninety ']
            
        if n == 0:
            return EMPTY
        if n > 19:
            return Y[n // 10] + X[n % 10] + suffix
        else:
            return X[n] + suffix
    except Exception as e:
        message = str(e)
        return message
 
def convert(n):
    try:
        result = convertToDigit((n // 1000000000) % 100, 'Billion, ')
        result += convertToDigit((n // 10000000) % 100, 'Crore, ')
        result += convertToDigit(((n // 100000) % 100), 'Lakh, ')
        result += convertToDigit(((n // 1000) % 100), 'Thousand, ')
        result += convertToDigit(((n // 100) % 10), 'Hundred ')
    
        if n > 100 and n % 100:
            result += 'and '
    
        result += convertToDigit((n % 100), '')
        return result.strip().rstrip(',').replace(', and', ' and')
    except Exception as e:
        message = str(e)
        return message

