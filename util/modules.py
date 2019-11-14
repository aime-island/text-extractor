import os
from reynir import Reynir
import PyPDF2 
from bs4 import BeautifulSoup, SoupStrainer
import enlighten
import time
import re
from util.normalization import (clean_text_from_xml, change_abbreviations, 
           change_numbers, segregation, segregation_for_language_model)

class directory_info():
    '''
    Class to hold information on current input data directories.
    '''
    def __init__(self, args, directory=None):
        #input_dir: the directory of the input folder
        #root_name: the name of the folder/file used for creating file names
        if directory:
            self.input_dir=directory
            self.root_name = directory[directory.rfind('\\')+1:]
        else:
            self.input_dir = args.input_dir
            self.root_name = args.input_dir[args.input_dir.rfind('\\')+1:]
    
    def get_root_name(self):
        return self.root_name
    
    def get_input_dir(self):
        return self.input_dir

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
    '''
    Simple class to create counter object
    '''
    def __init__(self):
        self.count_object = 0

    def iterate(self):
        self.count_object = self.count_object +1
    
    def show(self):
        return self.count_object

def create_directory():
    '''
    If the data directory is not present, create it!
    An error will occer if the data dir is only partially present.
    '''
    if not os.path.exists('.\data'):
        os.makedirs('.\data')
    if not os.path.exists('.\data\\01 - keep'):
        os.makedirs('.\data\\01 - keep')
    if not os.path.exists('.\data\\02 - notKeep'):
        os.makedirs('.\data\\02 - notKeep')
    if not os.path.exists('.\data\\03 - normalized'):
        os.makedirs('.\data\\03 - normalized')
    if not os.path.exists('.\data\\04 - clean'):
        os.makedirs('.\data\\04 - clean')
    if not os.path.exists('.\data\\05 - raw'):
        os.makedirs('.\data\\05 - raw')


def get_file_directories(args, from_where=None):
    '''
    Takes in a folder directory and datas a txt file and list with
    directories to all the file in that folder and its subfolder.
    '''
    dir_info = directory_info(args, from_where)
    input_dir = dir_info.get_input_dir()
    _root_name = dir_info.get_root_name()

    print(f'Getting list of files form {input_dir} and its subfolders')
    counter = Counter() 
    filepath_list = []
    for dirName, _subdirList, fileList in os.walk(input_dir, topdown=False):
        for fname in fileList:
            counter.iterate()
            filepath_list.append(dirName + '\\' + fname)  
        
    print(f'Done, found {counter.show()} files')
    #create_file(filepath_list, filename=f'List of file paths for {root_name}')
    return filepath_list

def create_file(data, filename='data.txt', mode='w'):
    '''
    Save a list to a file. Defult is "data.txt"
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

def call_extract_multible_xml(args):
    '''
    A specify extractor for multible xml files that keep their text in the 's' mark.
    The function extracts text form mulitble files and exports .txt files that have the names of the 
    subfolders in rootfolder.
    '''
    list_of_file_paths = get_file_directories(args)

    pbar = enlighten.Counter(total=len(list_of_file_paths), desc='Extracting files') 

    dir_info = directory_info(args)
    root_name = dir_info.get_root_name()
    name = get_subfolder_name(list_of_file_paths[0], root_name)

    list_to_create = []
    for path in list_of_file_paths:
        current_subfolder = get_subfolder_name(path, root_name)
        
        #Compare current subfolder to name. Given that the list_of_file_paths 
        #is linear this will create files with the names of the subfolder and
        #then reset the list_to_create      
        if name != current_subfolder or len(list_to_create) > 500:
            filename = '.\data\\05 - raw\\' + name +'.txt'
            create_file(list_to_create, filename, mode='a')
            list_to_create = []
            name = current_subfolder

        list_to_create.extend(xml_extractor(path))
    
        pbar.update()

    filename = '.\data\\05 - raw\\' + name +'.txt'
    create_file(list_to_create, filename, mode='a')
    
def get_file_length(path):
    with open(path, encoding='utf-8') as f: 
        length = sum(1 for line in open(path, encoding='utf-8'))
    return length

def call_xml_cleaner(args):
    '''
    Takes in a list of files and args and generates new files. 
    '''
    list_of_file_paths = get_file_directories(args)
    dir_info = directory_info(args)
    root_name = dir_info.get_root_name()

    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Tidying files:', unit='files')

    name = get_subfolder_name(list_of_file_paths[0], root_name)
    
    for path in list_of_file_paths:
        name = get_subfolder_name(path, root_name)
        filename = '.\data\\04 - clean\\' + name + '.txt'
        list_to_create = []
        currCenter = manager.counter(total=get_file_length(path), unit='lines', leave=False)
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

def call_nomrmalization_functions(args):
    '''
    Takes in a list of files and args and generates new files. 
    '''
    list_of_file_paths = get_file_directories(args)

    dir_info = directory_info(args)
    root_name = dir_info.get_root_name()

    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Tidying files:', unit='files')

    name = get_subfolder_name(list_of_file_paths[0], root_name)
    
    for path in list_of_file_paths:
        name = get_subfolder_name(path, root_name)
        filename = '.\data\\03 - normalized\\' + name +'.txt'
        list_to_create = []
        currCenter = manager.counter(total=get_file_length(path), unit='lines', leave=False)
        with open(path, encoding='utf-8') as file:
            for line in file:
    
                try:
                    line = change_abbreviations(line)
                    line = change_numbers(line)
                except:
                    pass
                
                list_to_create.append(line)
                if len(list_to_create) > 1000:
                    create_file(list_to_create, filename, mode='a') 
                    list_to_create = []
                
                currCenter.update()
        if list_to_create:
            create_file(list_to_create, filename, mode='a') 
        currCenter.close()
        enterprise.update()
    enterprise.close()

def call_segregation(args):
    
    '''
    In this funciton we want to segregate the sentences into two groups.
    The ones we want too use and the ones that don't meet our criteria. 
    '''

    list_of_file_paths = get_file_directories(args)
    dir_info = directory_info(args)
    root_name = dir_info.get_root_name()

    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Tidying files:', unit='files')

    name = get_subfolder_name(list_of_file_paths[0], root_name)
    
    for path in list_of_file_paths:
        name = get_subfolder_name(path, root_name)
        list_to_create = []
        list_to_create_not_keep = []

        currCenter = manager.counter(total=get_file_length(path), unit='lines', leave=False)
        with open(path, encoding='utf-8') as file:
            for line in file:
                
                if args.lm:
                    line, to_keep = segregation_for_language_model(line)
                else:
                    line, to_keep = segregation(line)                              
                
                if to_keep:
                    list_to_create.append(line)
                else:
                    list_to_create_not_keep.append(line)

                if len(list_to_create) > 1000:
                    filename = '.\data\\01 - keep\\' + name +'.txt'
                    create_file(list_to_create, filename, mode='a') 
                    list_to_create = []

                if len(list_to_create_not_keep) > 1000:
                    filename = '.\data\\02 - notKeep\\' + name +'.txt'
                    create_file(list_to_create_not_keep, filename, mode='a') 
                    list_to_create_not_keep = []

                currCenter.update()
    
        if list_to_create:
            filename = '.\data\\01 - keep\\' + name +'.txt'
            create_file(list_to_create, filename, mode='a') 

        if list_to_create_not_keep:
            filename = '.\data\\02 - notKeep\\' + name +'.txt'
            create_file(list_to_create_not_keep, filename, mode='a') 
        
            currCenter.close()
        enterprise.update()
    enterprise.close()

def call_combiner(args):
    '''
    In this funciton we combain all text files from a folder into one large file called merge
    '''

    print('Combining')
    list_of_file_paths = get_file_directories(args)
    manager = enlighten.get_manager()
    enterprise = manager.counter(total=len(list_of_file_paths), desc='Compinging files:', unit='files')
    list_to_create = []

    for path in list_of_file_paths:
        filename = '.\data\\merge.txt'

        currCenter = manager.counter(total=get_file_length(path), unit='lines', leave=False)
        with open(path, encoding='utf-8') as file:
            for line in file:

                list_to_create.append(line.strip())
           
                if len(list_to_create) > 1000:
                    create_file(list_to_create, filename, mode='a') 
                    list_to_create = []

                currCenter.update()
            currCenter.close()
    enterprise.update()

    if list_to_create:
        create_file(list_to_create, filename, mode='a') 

    enterprise.close()