import os
from reynir import Reynir
import PyPDF2 
from bs4 import BeautifulSoup, SoupStrainer
import re
import enlighten
import time
from tokenizer import tokenize, TOK
from util.num2words import convert_year_to_words



class Timer():
    '''
    Timer class for exicution time results.
    '''
    def __init__(self):
        self.startTime = time.time()
    
    def showTimer(self):
        runtime = round((time.time()-self.startTime)/60, 2)
        return(f'\nRuntime: {runtime} min\n')
        
class Counter():
    def __init__(self):
        self.count_object = 0

    def iterate(self):
        self.count_object = self.count_object +1
    
    def show(self):
        return self.count_object

def get_root_name(args):
    index = args.root_dir.rfind('\\')
    root_name = args.root_dir[index+1:]
    return root_name

def get_file_directories(args, from_where=None):
    '''
    Takes in a folder directory and outputs a txt file and list with
    directories to all the file in that folder and its subfolder.
    '''
    if from_where:
        directory = from_where
        root_name = from_where +'.txt'

    else:
        directory = args.root_dir
        root_name = get_root_name(args)+'.txt'

    print(f'Geting list of files form {directory} and its subfolders')
    counter = Counter() 
    filepath_list = []
    for dirName, _subdirList, fileList in os.walk(directory, topdown=False):
        for fname in fileList:
            counter.iterate()
            filepath_list.append(dirName + '\\' + fname)  
        
    print(f'Found {counter.show()} files')
    create_file(filepath_list, filename=f'List of file paths for {root_name}')
    return filepath_list

def create_file(data, filename='output.txt', mode='w'):
    '''
    Save a list to a file. Defult is "output.txt"
    print(f'Writing a file named: {filename}')
    '''

    if type(data) == list:
        with open(filename, mode, encoding='utf8') as file:
            for line in data:
                file.write(line + '\n')
    else: 
        with open(filename, mode, encoding='utf8') as file:
            file.write(data + '\n')

def open_file(filename, mode='r'):
    '''
    Opens a file named and returns a list with irs variables.
    '''
    print(f'Opening file: {filename}')
    list_to_return =[]
    with open(filename, mode, encoding='utf8') as file:
        for line in file:
            list_to_return.append(line.rstrip())
    return list_to_return   

def xml_extractor(file_directory):
    #print(f'Extracting sentences from {file_directory}')
    
    with open(file_directory, encoding="utf-8") as file:
        #Beacause s contains all the sentences
        soup = BeautifulSoup(file, 'lxml')
    
    sentences = soup.find_all('s') #Beacause s contains all the sentences 

    return [sentence.get_text().replace('\n', ' ') for sentence in sentences]

def create_directory():
    if not os.path.exists('.\outPut'):
        os.makedirs('.\outPut\\raw')
        os.makedirs('.\outPut\\clean')

def get_subfolder_name(directory, rootfolder):
    firstIndex = directory.index(rootfolder) + len(rootfolder)+1
    try:
        secondIndex = directory.index('\\', firstIndex)
    except:
        secondIndex = len(directory)

    name = re.sub('.xml|.txt', '', directory[firstIndex:secondIndex])
    return name

def extract_multible_xml(args, data):
    '''
    A specify extractor for multible xml files that keep their text in the 's' mark.
    The function extracts text form mulitble files and exports .txt files that have the names of the 
    subfolders in rootfolder.
    '''
    root_name = get_root_name(args)
    pbar = enlighten.Counter(total=len(data), desc='Extracting files') 
    name = get_subfolder_name(data[0], root_name)

    create_directory() #Create output directory

    list_to_create = []
    for path in data:
        current_subfolder = get_subfolder_name(path, root_name)
        
        #Compare current subfolder to name. Given that the list_of_file_paths 
        #is linear this will create files with the names of the subfolder and
        #then reset the list_to_create      
        if name != current_subfolder or len(list_to_create) > 500:
            filename = '.\outPut\\raw\\' + name +'.txt'
            create_file(list_to_create, filename, mode='a')
            list_to_create = []
            name = current_subfolder

        list_to_create.extend(xml_extractor(path))
    
        pbar.update()

    filename = '.\outPut\\raw\\' + name +'.txt'
    create_file(list_to_create, filename, mode='a')
    
def get_file_length(path):
    return sum(1 for line in open(path, encoding='utf-8'))

def normalization(sentence, args):
    for token in tokenize(sentence):
        if type(token.val) == list and args.abbr:
            sentence = sentence.replace(token.txt, token.val[0][0])

        if TOK.descr[token.kind] == 'YEAR' and args.nums:
            new_year = convert_year_to_words(token.val)
            
            if new_year != False:
                sentence = sentence.replace(str(token.val), new_year)
            else:
                print(f'Eitthvað að með árið: {token.val}' )
                #útfæra eitthvað hérna

        if TOK.descr[token.kind] == 'ORDINAL':
            print(token.val)
            print(TOK.descr[token.kind])
            print(token.txt)

    return sentence

def pick_apart_goose(s):
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

def between_years(s):
    for w in s.split():
        if re.match('[0-9]+ *- *[0-9]+', w):
            s = re.sub('-', ' til ', s)
    return s

def clean_text_from_xml(s):
    #s = re.sub(r'\n', ' ', s)
    s = re.sub('[\„|\“|\"]', '"', s)
    if re.search('.*".*"', s):
        s = pick_apart_goose(s)
    if re.search('[0-9]+(-)[0-9]+', s):
        s = between_years(s)
    s = re.sub('\s\. ', '.', s)
    s = re.sub('\s\$ ', '$', s)
    s = re.sub('\‘', '\'', s)
    s = re.sub('\s\?', '?', s)
    s = re.sub('\s\%', '%', s)
    s = re.sub('\s\!', '!', s)
    s = re.sub('\s\:', ':', s)
    s = re.sub('\s,', ',', s)
    s = re.sub('^\s', '', s)
    s = re.sub('\s\;', ';', s)
    s = re.sub('\(\s', '(', s)
    s = re.sub('\s\)', ')', s)
    s = re.sub('\s\/\s', '/', s)
    s = re.sub('\[\s', '[', s)
    s = re.sub('\s\]', ']', s)
    s = re.sub('\s\*', '*', s)
    s = re.sub('\'\s|\s\´', '\'', s)
    s = re.sub('\'\'', '', s)
    s = re.sub('\s$', '', s)
    s = re.sub('\s\-', '-', s)
    s = re.sub('\„\s', '„', s)
    s = re.sub('\s\“', '“', s)
    s = re.sub('\s\@', '@', s)
    s = re.sub('\s+', ' ', s)
    return s


def clean_text_from_xml_multiple(args, list_of_file_paths):
    '''
    Takes in a list of files and args and generates new files. 
    '''
    root_name = get_root_name(args)
    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Tidying files:')

    create_directory() #Create output directory

    name = get_subfolder_name(list_of_file_paths[0], root_name)
    
    for path in list_of_file_paths:

        name = get_subfolder_name(path, root_name)
        filename = '.\outPut\\clean\\' + name +'-clean.txt'
        list_to_create = []
        currCenter = manager.counter(total=get_file_length(path), unit='files', leave=False)
        with open(path, encoding='utf-8') as file:
            for line in file:
                list_to_create.append(clean_text_from_xml(line))
                if len(list_to_create) > 1000:
                    create_file(list_to_create, filename, mode='a') 
                    list_to_create = []
                
                currCenter.update()
        if list_to_create:
            create_file(list_to_create, filename, mode='a') 
        currCenter.close()
        enterprise.update()
    enterprise.close()    