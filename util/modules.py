import os
from reynir import Reynir
import PyPDF2 
from bs4 import BeautifulSoup, SoupStrainer
import re
import enlighten
import time


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

def get_file_directories(args, output_dir=None):
    '''
    Scarapes all files in the rootDir and its subfolders. 
    '''
    if output_dir:
        directory = output_dir
        root_name = 'cleaning'
    else:

        directory = args.root_dir
        root_name = args.root_name + '.txt'

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
    pbar = enlighten.Counter(total=len(data), desc='Extracting files') 
    name = get_subfolder_name(data[0], args.root_name)
    

    list_to_create = []
    for path in data:
        current_subfolder = get_subfolder_name(path, args.root_name)
        
        #Compare current subfolder to name. Given that the list_of_file_paths 
        #is linear this will create files with the names of the subfolder and
        #then reset the list_to_create      
        if name != current_subfolder or len(list_to_create) > 50:
            filename = '.\outPut\\raw\\' + name +'.txt'
            create_file(list_to_create, filename, mode='a')
            list_to_create = []
            name = current_subfolder

       
        list_to_create.extend(xml_extractor(path))


        pbar.update()
    filename = '.\outPut\\raw\\' + name +'.txt'
    create_file(list_to_create, filename, mode='a')


def clean_multiple_files(args, list_of_file_paths):
    '''
    Takes in a list of files and args and generates new files that have been cleand
    using reynir. 
    '''
    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Tidying files:')

    name = get_subfolder_name(list_of_file_paths[0], 'raw')
    
    for path in list_of_file_paths:

        name = get_subfolder_name(path, 'raw')
        filename = '.\outPut\\clean\\' + name +'-clean.txt'
        list_to_create = []
        currCenter = manager.counter(total=get_file_length(path), unit='files', leave=False)
        with open(path, encoding='utf-8') as file:
            for line in file:
                if len(line) > 600:
                    file_name =  '.\outPut\\' + name +'-too-long.txt'

                    create_file(line.rstrip(), file_name, mode='a')
                
                else:
                    list_to_create.extend(list(reynir_tidy_text(line)))

                    if len(list_to_create) > 1000:
                        create_file(list_to_create, filename, mode='a') 
                        list_to_create = []
                
                currCenter.update()
        if list_to_create:
            create_file(list_to_create, filename, mode='a') 
        currCenter.close()
        enterprise.update()
    enterprise.close()
    
    
def get_file_length(path):
    return sum(1 for line in open(path, encoding='utf-8'))

def reynir_tidy_text(data):
    '''
    Takes a list or a string and returns a list of str with a text representation 
    of the sentence, with correct spacing between tokens, and em- and en-dashes 
    substituted for regular hyphens as appropriate. 
    '''
    list_to_return = []
    r = Reynir() 
    if type(data) == list:
        #print('Tidying list of sentences')

        # Initialize Reynir and submit the text as a parse job
        for line in data:
            job = r.submit(line)

            # Iterate through sentences and parse each one
            for item in job:
                item.parse()
                list_to_return.append(item.tidy_text)

    elif type(data) == str:
        #print('Tidying a string')
        job = r.submit(data)
        for item in job:
            item.parse()
            list_to_return.append(item.tidy_text)
    else:
        print('reynir_tidy_text only takes a list or a string\nFor this blasphemy I return you a empty list')


    return list_to_return