from tokenizer import tokenize, TOK
from reynir import Reynir
import re
import random


#from num2words import convert_numbers_to_words
#from num2words_ordinal import convert_ordinal_to_words

from util.num2words import convert_numbers_to_words
from util.num2words_ordinal import convert_ordinal_to_words

r = Reynir() #!!! Reynir takes up about 60mb for every instance. This might not 
             #be a good enough idea.

list_of_bad_words = [line.strip() for line in open(r'.\util\badwords.txt', encoding='utf-8')]

allowed_symbols = [':',',','!','?','.','-','„','“','"', ' ','\n']
allowed_letters_samll = ['A','Á','B','D','Ð','E','É','F','G','H','I','Í','J',
    'K','L','M','N','O','Ó','P','R','S','T','U','Ú','V','X','Y','Ý','Þ','Æ','Ö']
allowed_letters_big = ['a','á','b','d','ð','e','é','f','g','h','i','í','j',
    'k','l','m','n','o','ó','p','r','s','t','u','ú','v','x','y','ý','þ','æ','ö']

def change_abbreviations(s):
    #We match if the patter ex. m.a. is in text or ex. heilbriðigsr. 
    #We may miss a few if the the abbr are in the end of senteces
    #but that is worth the increace in speed as tokenizing every sentece is 
    #timeconsuming
    if (re.search('\w\.\w\.', s)) or (re.search('\w+\.', s[:-1])):
        for token in tokenize(s):
            if type(token.val) == list:
                s = s.replace(token.txt, token.val[0][0])

        #some common abbr that the tokenizer dose't spot
        s = re.sub('m\.a\s', 'meðal annars', s)
        s = re.sub('þ\.e\.a\.s', 'það er að segja', s)
        s = re.sub('(f\.kr\.{0,1})|(f\.Kr\.{0,1})', 'fyrir krist', s)
        s = re.sub('\s\s', ' ', s)

    return s.strip()


def change_numbers(s):
    #If there are numbers in the sentence we want to take some action 
    #to change them to written words.

    #ORDNIAL
    Gender = ['hk', 'kvk', 'kk']
    while re.search('[0-9]{1,4}\.\s', s): 
        gender = Gender[random.randint(0,2)]
        ordnial = re.search('[0-9]{1,4}\.\s', s).group(0)
        
        s = s.replace(ordnial, convert_ordinal_to_words(ordnial, ['NF', gender]) + ' ')

    #Prósentur
    while re.search('[0-9]{0,2}[\,|\.]{0,1}[0-9]{0,2}\s*\%', s):
        orginal_num = re.search('[0-9]{0,2}[\,|\.]{0,1}[0-9]{0,2}\s*\%', s).group(0)
        nums = re.sub('%', '', orginal_num)
        nums = re.sub('\s', '', nums)
        if re.search(',', nums):
            nums  = nums.split(',')
        elif re.search('\.', nums):
            nums  = nums.split('.')

        new_nums = []
        for num in nums:
            new_nums.append(convert_numbers_to_words(num))

        if len(new_nums) > 1:
            new_nums[-1]= 'komma'
        new_nums = new_nums + ['prósent']

        new_nums = ' '.join(new_nums)
        s = s.replace(orginal_num, new_nums)
    
    #tölur minni en 999
    while re.search('\s\d{1,3}\s', s):
        num = re.search('\s\d{1,3}\s', s).group(0)
        new_num = ' ' + convert_numbers_to_words(num) + ' '
        s = s.replace(num, new_num, s)
    return s        

    '''
    if re.search('\s[0-9]+', s):
        for token in tokenize(s):
            
            #Changing years we call the method convert_numbers_to_words
            if TOK.descr[token.kind] == 'YEAR':
                #print(f'Hérna er token.val {type(token.val)}')
                new_year = convert_numbers_to_words(token.val, is_year = True)
                if new_year != False:
                    s = s.replace(str(token.val), new_year)
                else:
                    #This else statement is raised if the year is higher
                    #then 9999, that should be an execption. Their also 
                    #a chance that some other edge cases raise make the 
                    #method convert_numbers_to_words return False.
                    print(f'Eitthvað að með árið: {token.txt}\n{s}' )
            
            #if the number is an ordinal ex. 1. sæti.
            if TOK.descr[token.kind] == 'ORDINAL':
                sent = r.parse_single(s).terminals
                if sent != None:
                    for t in sent:
                        #print(t)
                        if t.category == 'raðnr' and len(t.variants) != 0:
                            #print(t.variants, token.txt, token.val)
                            s = s.replace(str(token.txt), convert_ordinal_to_words(token.txt, t.variants))
                            break 
                else:
                    s = s.replace(str(token.txt), convert_ordinal_to_words(token.txt))
            
            if TOK.descr[token.kind] == 'NUMBER' and re.match('\d{1,4}', token.txt) != None:
                new_number = convert_numbers_to_words(token.val)
                #print(f'hérna token.val líka {type(token.val)}')
                if new_year != False:
                    s = s.replace(str(token.val), new_number)
                else:
                    #This else statement is raised if the year is higher
                    #then 9999, that should be an execption. Their also 
                    #a chance that some other edge cases raise make the 
                    #method convert_numbers_to_words return False.
                    print(f'Eitthvað að með árið: {token.txt}\n{s}' )
    '''

    return s    

def pick_apart_goose(s):
    #Auðvita þýðast gæsalappir sem goose. 
    first = True
    w = ''
    for letter in s:
        if letter == '"' and first:
            w = w + (' „')
            first = False
        elif letter == '"' and not first:
            w = w + ('“ ')
            first = True
        else:
            w = w + letter
    return w

def hyphen_between_numbers(s):
    #Fix space between hyphen of numbers.
    #Ex. 1994 - 1995 will be 1994-1995.
    if re.search('[0-9]+\s*-\s*[0-9]+', s):
            s = re.sub('\s\-\s', '-', s)
    return s    

def clean_text_from_xml(s):
    #s = re.sub(r'\n', ' ', s)

    #Tek burt bil í upphafi og enda setningar
    s = re.sub('^\s', '', s)
    s = re.sub('\s$', '', s)

    #Set allar gæsalappir sem enskar gæsalappir og
    #skipiti þeim síðan út fyrir íslenskra. Virkar 90%.
    s = re.sub('[\„|\“|\"]', '"', s)
    if re.search('.*".*"', s):
        s = pick_apart_goose(s)
    s = re.sub('\„\s', '„', s)
    s = re.sub('\s\“', '“', s)

    #Ef það eru fleiri en ein setnig í línu.
    s = re.sub('\s\.\s', '.\n', s)
    s = re.sub('\s\?\s', '?\n', s)
    s = re.sub('\s\!\s', '!\n', s)

    #Laga bandstrik
    s = hyphen_between_numbers(s)
    s = re.sub('\s\-', '-', s)

    
    #Tek burtu bil í kringum sviga, hornklofa og önnur tákn
    s = re.sub('\(\s', '(', s)
    s = re.sub('\s\)', ')', s)
    s = re.sub('\s\/\s', '/', s)
    s = re.sub('\[\s', '[', s)
    s = re.sub('\s\]', ']', s)
    

    #Tek burtu bil á undan punkti og öðrum táknum
    s = re.sub('\s\.', '.', s)
    s = re.sub('\'\s|\s\´', '\'', s)
    s = re.sub('\s\$ ', '$', s)
    s = re.sub('\s\?', '?', s)
    s = re.sub('\s\%', '%', s)
    s = re.sub('\s\!', '!', s)
    s = re.sub('\s\:', ':', s)
    s = re.sub('\s,', ',', s)
    s = re.sub('\s\;', ';', s)
    s = re.sub('\s\*', '*', s)
    s = re.sub('\s\@', '@', s)
    s = re.sub('\“\s\.', '“.', s)

    #Tek burtu tákn
    s = re.sub('\'\'', '', s)
    s = re.sub('\‘', '\'', s)
    s = re.sub('^"\s', '', s)
    s = re.sub('\,\,', '', s)

    #Tek burtu auk bil ef það eru tvö eða fleiri
    s = re.sub('\s{2,}', ' ', s)
    return s

def right_length(s):
    length = len(s.split(' '))
    if length > 2 and length < 14:
        return True
    else:
        False

def no_bad_words(s):
    for word in s.split(' '):
        if word in list_of_bad_words:
            return False
    return True

def remove_brackets(s):
    #Remove everything within parentheses or brackets    
    s = re.sub(r'([\(\[\<]).*?([\)\]\>])', '', s)
    s = re.sub('\s{2,}', ' ', s)
    s = re.sub('\n{2,}', '\n', s)
    return s

def segregation(s):
    s = remove_brackets(s)
    allowed_symbols_and_letters = allowed_symbols + allowed_letters_samll + allowed_letters_big
    
    only_allowed_letters = True
    for l in s: 
        if l not in allowed_symbols_and_letters:
            only_allowed_letters = False 
            break

    if right_length(s) and only_allowed_letters and no_bad_words(s):
        to_keep = True
    else:
        to_keep = False

    return s.strip(), to_keep


def segregation_for_language_model(s):
    s = remove_brackets(s)

    allowed_symbols_and_letters = allowed_symbols + allowed_letters_samll + allowed_letters_big

    only_allowed_letters = True
    for l in s: 
        if l not in allowed_symbols_and_letters:
            only_allowed_letters = False 
            break

    if only_allowed_letters:
        to_keep = True
    else:
        to_keep = False

    return s.strip(), to_keep

