import re
from tokenizer import tokenize, TOK
import math

conjunction = "og"

gender_difference = {'KK': 'i', 'KVK': 'a', 'HK':'a'}

tens_power = {'100': 'hundraðast', '1000':'þúsundast'} 

tens_multiple = ['', 'tíund','tuttugast', 'þrítugast', 'fertugast',
            'fimmtugast', 'sextugast', 'sjötugast', 
            'áttugast', 'nítugast']

two_digits = ['', 'elleft', 'tólft', 'þrettánd', 
            'fjórtánd', 'fimmtánd', 'sextánd', 
            'sautjánd', 'átjánd', 'nítjánd']

single_digit_fem = ['núll', "eitt", "tvö", "þrjú", 
                'fjögur', "fimm", "sex",
                "sjö", "átta", "níu"] 

single_digits = {'KK': ['', "", "", "þriðji", 
                        "fjórði", "fimmti", "sjötti", 
                        "sjöundi", 'áttundi', "níundi"],

                'KVK': ['', '', '', "þriðja", 
                        "fjórða", "fimmta", "sjötta", 
                        "sjöunda", "áttunda", "níunda"],
                        
                'HK': ['', "", "", "þriðja", 
                        "fjórða", "fimmta", "sjöttö", 
                        "sjöunda", "áttunda", "níunda"],
                
                '1': 
                {'KK': {'NF': 'fyrsti', 'ÞF': 'fyrsta', 'ÞGF': 'fyrsta', 'EF': 'fyrsta'},
                'KVK': {'NF': 'fyrsta', 'ÞF': 'fyrstu', 'ÞGF': 'fyrstu', 'EF': 'fyrstu'},
                'HK': {'NF': 'fyrsta', 'ÞF': 'fyrsta', 'ÞGF': 'fyrsta', 'EF': 'fyrsta'}},

                '2': 
                {'KK': {'NF': 'annar', 'ÞF': 'annan', 'ÞGF': 'öðrum', 'EF': 'annars'},
                'KVK': {'NF': 'önnur', 'ÞF': 'aðra', 'ÞGF': 'annarri', 'EF': 'annarrar'},
                'HK': {'NF': 'annað', 'ÞF': 'annað', 'ÞGF': 'öðru', 'EF': 'annars'}}
                }

def is_devisable_ordinal(num, gender):
    i = int(num)
    if i % 1000 == 0:
        return (tens_power['1000'] + gender_difference[gender])
    if i % 100 == 0:
        return (tens_power['100'] + gender_difference[gender])
    if i % 10 == 0:
        return (tens_multiple[int(num[0])] + gender_difference[gender])
    else: 
        return False


def single_digits_getter(num, gender, conjugation):
    l = len(num)
    if num[0] == '0' and l == 2:
        num = num[1]
        l = len(num)

    if (l == 1) or (num[0] == '0'):
        if num in ['1','2']:
            return single_digits[num][gender][conjugation]
        else:
            return single_digits[gender][int(num)]
    else:
        return False

def add_conjunction(num, listWords, gender):
    l = len(num)
    if l > 1 and is_devisable_ordinal(num, gender) == False and num not in two_digits:
        listWords[-1:-1] = ['og']

    return (' '.join(listWords)) 


def convert_ordinal_to_words(num, genderAndConjugation = ['NF', 'HK']):
    num = re.sub('\.', '', num)
    num = re.sub(' ', '', num)
    conjugation, gender = list(map(lambda x:x.upper(), genderAndConjugation))
    
    num = str(num)
    orgNum = num 
    l = len(num)
    i = int(num)

    # Boundries
    if (l == 0) or (l > 4): 
        print(f'Out of boundry: {num}')
        return False

    # For single digit number  
    is_singal = single_digits_getter(num, gender, conjugation)
    if is_singal != False:
        return is_singal
        
    # Iterate while num is not 
    words = []  
    while (0 < len(num)):
        l = len(num)

        is_dev = is_devisable_ordinal(num, gender)
        if is_dev != False:
            words.append(is_dev)
            break
        
        if (l == 4):
            words.append(single_digit_fem[int(num[0])] +
                ' ' + tens_power['1000'] + gender_difference[gender])
        
        if l == 3:
            if num[0] == '0':
                pass
            else: 
                words.append(single_digit_fem[int(num[0])] +
                    ' ' + tens_power['100'] + gender_difference[gender])

        if l == 2:
            if num[0] == '0':
                words.append(single_digits_getter(num, gender, conjugation))
                break
            elif int(num) > 19:
                words.append(tens_multiple[int(num[0])] + gender_difference[gender])
                words.append(single_digits_getter(num[1], gender, conjugation))
                break
            else:
                words.append(two_digits[int(num[1])] + gender_difference[gender])
                break
        
        num = num[1:]
    return add_conjunction(orgNum, words, gender)