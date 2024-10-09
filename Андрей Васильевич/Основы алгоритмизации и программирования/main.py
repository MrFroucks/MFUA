def convert_bin(num):
    split_parts = num.split('.')
    one_num = split_parts[0]
    bin_one_num = bin(int(one_num))[2:]
    two_num = split_parts[1]
    bin_two_num = ''
    decimal_part = float('0.' + two_num)
    while decimal_part > 0 and len(bin_two_num) < 10: 
        decimal_part *= 2
        if decimal_part >= 1:
            bin_two_num += '1'
            decimal_part -= 1
        else:
            bin_two_num += '0'
    return f'{bin_one_num}.{bin_two_num}' 


def covert_oct(num):
    split_parts = num.split('.')
    one_num = split_parts[0]
    oct_one_num = oct(int(one_num))[2:]
    if len(split_parts) > 1:
        two_num = split_parts[1]
        oct_two_num = ''
        decimal_part = float('0.' + two_num)
        while decimal_part > 0 and len(oct_two_num) < 10:
            decimal_part *= 8
            digit = int(decimal_part)
            oct_two_num += str(digit)
            decimal_part -= digit
        return f'{oct_one_num}.{oct_two_num}'
    return oct_one_num


def convert_dec(num):
    pass


def determine_base(num):
    if '.' in num:
        whole_part, fractional_part = num.split('.')
    else:
        whole_part = num
        fractional_part = ''
        
    if any(char in whole_part for char in '89'):
        return 10
    elif any(char in whole_part for char in '01234567'):
        return 8
    elif any(char in whole_part for char in '01'):
        return 2
    elif any(char in whole_part for char in '0123456789ABCDEF'):
        return 16
    else:
        return 'unk'
        
        
def MAIN():
    num = input('Переводимое число>> ')
    s = determine_base(num)
    if ',' in num:
        num = num.replace(',', '.', 1)
        
    if '.' in num:
        bin_num = convert_bin(num)
        oct_num = covert_oct(num)
    else:
        bin_num = bin(int(num))[2:]
        oct_num = oct(int(num))[2:]
        dec_num = int(num, s)
    print(f'BIN: {bin_num}\nOCT: {oct_num}\nDEC: {dec_num}')


if __name__ == '__main__':
    MAIN()