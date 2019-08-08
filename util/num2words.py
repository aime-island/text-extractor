import math

conjunction = "og"
        
tens_power = ['hundrað', 'þúsund', 'hundruð'] 

tens_multiple = ['', '','tuttugu', 'þrjátíu', 'fjörutíu',
                'fimmtíu', 'sextíu', 'sjötíu', 
                'áttatíu', 'níutíu']

two_digits = ['tíu', 'ellefu', 'tólf', 'þrettán', 
                'fjórtán', 'fimmtán', 'sextán', 
                'sautján', 'átján', 'nítján']

single_digits = ["núll", "einn", "tveir", 
                "þrír", "fjórir", "fimm", 
                "sex", "sjö", "átta", "níu"]            

single_digits_fem = ['núll', "eitt", "tvö", "þrjú", 
                    'fjögur', "fimm", "sex",
                    "sjö", "átta", "níu"]

def is_devisable(num):
    i = int(num)
    if i % 1000 == 0:
        return (single_digits_fem[int(num[0])] + ' ' + tens_power[1])
    if i % 100 == 0:
        return (single_digits_fem[int(num[0])] + ' ' + tens_power[0])
    if i % 10 == 0:
        return two_digits[1]
    else: 
        return False

def add_conjunction(num, listWords):
    l = len(num)
    if l > 1 and is_devisable(num) == False and num not in two_digits:
        listWords[-1:-1] = ['og']
 

    return (' '.join(listWords)) 


# given number in words  
def convert_year_to_words(num): 
    
    #max year is 9999
    if int(num) > 9999:
        return False    

    num = str(num)
    orgNum = num 
    l = len(num)
    i = int(num)

  
    # Base cases  
    if (l == 0): 
        return False
  
    if (l > 4): 
        return False
    
    # For single digit number  
    if (l == 1):
        return single_digits_fem[i]
        
    # Iterate while num is not '\0'
    words= []  
    while (0 < len(num)):
        l = len(num)

        is_dev = is_devisable(num)
        if is_dev != False:
            words.append(is_dev)
            break
        
        if 2000 > int(num) > 1000:
            #print(f'Hérna {num}')
            words.append(two_digits[int(num[1])] + 
                        ' ' + tens_power[2])
            num = num[2:]
            l = len(num)

        if l == 4:
            #print('l === 4')
            words.append(single_digits_fem[int(num[0])] +
                ' ' + tens_power[1])

        if l == 3:
            #print('l == 3')
            if num[0] == '0':
                pass
            else: 
                words.append(single_digits_fem[int(num[0])] +
                    ' ' + tens_power[0])

        if l == 2:
            #print('l == 2')
            if num[0] == '0':
                words.append(single_digits_fem[int(num[1])])
                break
            elif int(num) > 19:
                words.append(tens_multiple[int(num[0])])
                words.append(single_digits_fem[int(num[1])])
                break
            else:
                words.append(two_digits[int(num[1])])
                break

        if l == 1:
            #print('l == 1')
            words.append(single_digits[int(num[0])])
            break

        num = num[1:]
       
        
    return add_conjunction(orgNum, words)



